import os
import sys
from pathlib import Path

import docker
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from stream_formatter import print_stream

load_dotenv()
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

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

agent = create_agent(
    model=llm_openai,
    tools=tools,
    system_prompt="""You are a Manim video generation agent. You create mathematical/explainer videos using the Manim library.

You have access to a Docker container with Manim pre-installed. Use the tools to:
1. Write a Python file defining a Manim scene (use manim's Scene class and self.play())
2. Run manim to render it: `manim -qm scene.py SceneName` (-qm = medium quality, 720p)
3. Use fetch_video to copy the rendered video from media/videos/... to the host
4. Report the final video path to the user

Manim outputs to media/videos/<filename>/<resolution>/<SceneName>.mp4. Always call fetch_video after rendering.""",
)

VIDEO_PROMPT = (
    sys.argv[1]
    if len(sys.argv) > 1 and sys.argv[1]
    else "Create a video explaining the pythagorean theorem."
)

stream = agent.stream(
    {"messages": [{"role": "user", "content": VIDEO_PROMPT}]},
    stream_mode="values",
)
print_stream(stream)

# Clean up container when done:

container.stop()
container.remove()