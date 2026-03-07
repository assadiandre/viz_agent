import os
import sys
from pathlib import Path

import docker
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph_reflection import create_reflection_graph

from stream_formatter import print_stream

load_dotenv()
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

client = docker.from_env()

# Output directory for generated videos (bind-mounted into container at /output)
OUTPUT_DIR = Path("./output").resolve()
OUTPUT_DIR.mkdir(exist_ok=True)

# SETUP THE CONTAINER
# Run as root so we can write to /workspace (Manim image defaults to manimuser)
container = client.containers.run(
    "viz-agent-manim",
    detach=True,
    user="root",
    working_dir="/workspace",
    volumes={
        "agent_workspace": {"bind": "/workspace", "mode": "rw"},
        str(OUTPUT_DIR): {"bind": "/output", "mode": "rw"},
    },
)

# THIS IS NEEDED SO THAT WE DONT END UP WITH DOUBLE /workspace IN THE PATHS
def _workspace_path(path: str) -> str:
    """Normalize path to be relative to /workspace (avoids double /workspace/)."""
    p = path.lstrip("/").replace("/workspace/", "").replace("workspace/", "")
    return p or "."


# SOME TOOLS WEVE DEFINED
@tool
def run_command(command: str) -> str:
    """Execute a shell command in the Docker container."""
    exit_code, output = container.exec_run(cmd=["bash", "-c", command])
    return f"Exit code: {exit_code}\n{output.decode()}"

@tool
def write_file(path: str, content: str) -> str:
    """Write a file inside the Docker container. Path can be relative (e.g. 'scene.py') or absolute ('/workspace/scene.py')."""
    clean = _workspace_path(path)
    exit_code, output = container.exec_run(
        cmd=["bash", "-c", f"cat > /workspace/{clean} << 'FILEEOF'\n{content}\nFILEEOF"]
    )
    return f"Wrote {clean}" if exit_code == 0 else f"Error: {output.decode()}"

@tool
def read_file(path: str) -> str:
    """Read a file from the Docker container. Path can be relative or absolute (/workspace/...)."""
    clean = _workspace_path(path)
    exit_code, output = container.exec_run(cmd=["cat", f"/workspace/{clean}"])
    return output.decode() if exit_code == 0 else f"Error: {output.decode()}"

@tool
def list_files(path: str = ".") -> str:
    """List files in a directory inside the Docker container. Path can be relative or absolute (/workspace/...)."""
    clean = _workspace_path(path)
    exit_code, output = container.exec_run(cmd=["ls", "-la", f"/workspace/{clean}"])
    return output.decode()


@tool
def fetch_video(container_path: str) -> str:
    """Copy a video file from the container to the host output directory.
    Pass the path in the container, e.g. 'media/videos/scene/1080p60/Scene.mp4'
    (relative to /workspace) or '/tmp/media/videos/...' (absolute).
    Returns the absolute path to the video on the host."""
    clean = _workspace_path(container_path)
    filename = os.path.basename(clean)
    if container_path.startswith("/") and not container_path.startswith("/workspace"):
        src = container_path
    else:
        src = f"/workspace/{clean}"
    dst = f"/output/{filename}"
    exit_code, output = container.exec_run(cmd=["cp", src, dst])
    if exit_code != 0:
        return f"Error copying video: {output.decode()}"
    host_path = OUTPUT_DIR / filename
    return str(host_path)

# def extract_written_code(messages: list) -> list[tuple[str, str]]:
#     """Extract (path, content) from write_file tool calls. Returns most recent .py files first."""
#     results = []
#     for m in messages:
#         if not isinstance(m, AIMessage) or not getattr(m, "tool_calls", None):
#             continue
#         for tc in m.tool_calls:
#             if tc.get("name") == "write_file":
#                 args = tc.get("args", {})
#                 path = args.get("path", "")
#                 content = args.get("content", "")
#                 if path.endswith(".py") and content:
#                     results.append((path, content))
#     return results

# DEFINE THE AGENT

tools = [run_command, write_file, read_file, list_files, fetch_video]

# Initialize the LLM
llm_anthropic = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=ANTHROPIC_API_KEY,
)

llm_openai = ChatOpenAI(
    model="gpt-5.2-codex",
    api_key=OPENAI_API_KEY,
)

llm_google = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    api_key=GEMINI_API_KEY,
)


# DEFINE THE VIDEO GENERATION AGENT
video_generation_agent = create_agent(
    model=llm_anthropic,
    tools=tools,
    system_prompt="""You are a Manim video generation agent. You create mathematical/explainer videos using the Manim library.

You have access to a Docker container with Manim pre-installed. Use the tools to:
1. Write a Python file defining a Manim scene (use manim's Scene class and self.play())
2. Run manim to render it: `manim -qm scene.py SceneName` (-qm = medium quality, 720p)
3. Use fetch_video to copy the rendered video from media/videos/... to the host
4. Report the final video path to the user

Manim outputs to media/videos/<filename>/<resolution>/<SceneName>.mp4. Always call fetch_video after rendering.

When you receive feedback from the critic, revise your video accordingly. Address each point in the feedback.""",
)

# DEFINE THE CRITIC (JUDGE) NODE
# The critic evaluates the video agent's work and returns feedback to trigger revision, or nothing to finish.
CRITIC_PROMPT = """You are a critic evaluating a Manim explainer video. You cannot watch the actual video, but you can evaluate:
- The Manim scene code (animations, structure, clarity)
- Whether the agent followed the user's request
- Mathematical correctness and pedagogy
- Pacing and visual design choices in the code

Based on the conversation below (which includes the agent's code, commands, and results):

If the work is satisfactory and complete, reply with exactly: APPROVED

If improvements are needed, reply with: REVISE:
Then give specific, actionable feedback for the video generation agent to fix. Be concrete (e.g. "Add a fade-in to the formula", "The triangle labels are wrong - use A, B, C at vertices").
"""


def _get_code_from_container() -> str:
    """Read all .py files from /workspace in the container. Returns combined code or empty if none."""
    listing = list_files.invoke({"path": "."})
    # Parse "ls -la" style output for .py filenames (e.g. "-rw-r--r-- 1 root root 1234 ... scene.py")
    py_files = []
    for line in listing.split("\n"):
        parts = line.split()
        if len(parts) >= 9 and parts[-1].endswith(".py") and not parts[-1].startswith("."):
            py_files.append(parts[-1])
    if not py_files:
        return "(no .py files found in workspace)"
    combined = []
    for path in py_files:
        content = read_file.invoke({"path": path})
        if not content.startswith("Error"):
            combined.append(f"# --- {path} ---\n{content}")
    return "\n\n".join(combined) if combined else "(could not read any .py files)"


def judge_video(state: dict) -> dict | None:
    """Evaluate the video agent's output. Return feedback to trigger revision, or None to approve."""
    messages = state.get("messages", [])
    if not messages:
        return None

    # Get user request and code from container (Option 2)
    user_request = next(
        (m.content for m in messages if isinstance(m, HumanMessage) and not str(m.content).startswith("Critic feedback")),
        "",
    )
    code_from_container = _get_code_from_container()
    print("CODE FROM CONTAINER: ", code_from_container)
    # critic_input = f"""[User request]
    # {user_request}

    # [Code in container - current state of /workspace]
    # {code_from_container}
    # """

    # response = llm_google.invoke(
    #     [{"role": "system", "content": CRITIC_PROMPT}, {"role": "user", "content": critic_input}]
    # )
    # raw = response.content if hasattr(response, "content") else str(response)
    # content = raw.strip()

    # # If critic says REVISE:, extract feedback and loop back to video agent
    # if "REVISE:" in content.upper():
    #     idx = content.upper().index("REVISE:")
    #     feedback = content[idx + len("REVISE:") :].strip()
    #     return {"messages": [HumanMessage(content=f"Critic feedback – please revise the video:\n\n{feedback}")]}
    # Otherwise treat as approved – no new message, reflection loop ends
    return None


# Build the critic (reflection) graph
critic_graph = (
    StateGraph(MessagesState)
    .add_node("judge", judge_video)
    .add_edge(START, "judge")
    .add_edge("judge", END)
    .compile()
)

# Create the reflection loop: video_agent <-> critic until approved
# Pass state_schema explicitly to avoid langgraph_reflection's graph.builder.schema (removed in langgraph 1.x)
reflection_app = create_reflection_graph(
    video_generation_agent, critic_graph, state_schema=MessagesState
).compile()

VIDEO_PROMPT = (
    sys.argv[1]
    if len(sys.argv) > 1 and sys.argv[1]
    else "Create a video displaying a circle"
)

stream = reflection_app.stream(
    {"messages": [{"role": "user", "content": VIDEO_PROMPT}]},
    stream_mode="values",
    config={"recursion_limit": 50},
    subgraphs=True,
)
print_stream(stream)

# Clean up container when done:

container.stop()
container.remove()