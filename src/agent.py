import re

from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph

from .config import (
    ANTHROPIC_API_KEY,
    CODING_PROMPT,
    CRITIC_PROMPT,
    GOOGLE_API_KEY,
    HARDCODED_PLAN,
    OPENAI_API_KEY,
    PLANNER_PROMPT_V3,
    RENDER_PROMPT,
    SYSTEM_PROMPT,
    XAI_API_KEY,
)
from .tools import get_coding_tools, get_critic_tools, get_render_tools

MAX_CRITIC_ROUNDS = 0  # temporarily disabled

llm_anthropic = ChatAnthropic(
    model="claude-opus-4-6",
    api_key=ANTHROPIC_API_KEY,
)

llm_openai = ChatOpenAI(
    model="gpt-5.3-codex",
    api_key=OPENAI_API_KEY,
)

llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-3.1-pro-preview",
    google_api_key=GOOGLE_API_KEY,
)

llm_grok = ChatOpenAI(
    model="grok-code-fast-1",
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)


def _build_llm_agent(tools, *, llm=None, system_prompt=SYSTEM_PROMPT):
    """Create one LangChain agent node."""
    return create_agent(
        model=llm or llm_openai,
        tools=tools,
        system_prompt=system_prompt,
    )


def _extract_text(content) -> str:
    """Normalise AI message content to a plain string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    return str(content)


def _parse_scenes(planner_output: str) -> list[str]:
    """Split planner output into individual scene descriptions.

    Scenes are delimited by top-level numbered headers of the form
    ``N. PascalCaseName`` at the start of a line (e.g. ``2. GeometricSquares``).
    Falls back to treating the whole output as a single scene if no such
    headers are found.
    """
    parts = re.split(r"(?=^\d+\.\s+[A-Z]\w*)", planner_output, flags=re.MULTILINE)
    scenes = [s.strip() for s in parts if s.strip() and re.match(r"^\d+\.", s.strip())]
    return scenes or [planner_output.strip()]


def _is_approved(messages) -> bool:
    """Check if the critic's final AI response contains an approval verdict."""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage):
            text = _extract_text(msg.content).upper()
            return "VERDICT: APPROVE" in text
    return False


def build_agent(*, llm=None):
    """Create a StateGraph: planner -> (code -> critic loop -> render) per scene."""

    def planner_agent(state: MessagesState) -> MessagesState:
        return {"messages": state["messages"] + [AIMessage(content=HARDCODED_PLAN)]}

    coding_agent = _build_llm_agent(
        get_coding_tools(), llm=llm_gemini, system_prompt=CODING_PROMPT
    )
    critic_agent = _build_llm_agent(
        get_critic_tools(), llm=llm_anthropic, system_prompt=CRITIC_PROMPT
    )
    render_agent = _build_llm_agent(
        get_render_tools(), llm=llm_openai, system_prompt=RENDER_PROMPT
    )

    def _run_scenes_sequentially(state: MessagesState) -> MessagesState:
        planner_text = _extract_text(state["messages"][-1].content)
        scenes = _parse_scenes(planner_text)
        all_messages = list(state["messages"])

        print(f"SCENE COUNT: {len(scenes)}")

        for i, scene in enumerate(scenes, 1):
            print(f"\n{'='*60}")
            print(f"SCENE {i}/{len(scenes)}")
            print(f"{'='*60}")

            # --- Step 1: Code the scene (no rendering) ---
            print("[CODING] Writing scene...")
            code_result = coding_agent.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content=(
                                "Implement the following scene as a complete, "
                                "self-contained Manim Python file.\n\n"
                                f"{scene}"
                            )
                        )
                    ]
                }
            )
            all_messages += code_result["messages"]

            # --- Step 2: Critic feedback loop ---
            for round_num in range(MAX_CRITIC_ROUNDS):
                print(
                    f"[CRITIC] Review round {round_num + 1}/{MAX_CRITIC_ROUNDS}..."
                )
                critic_result = critic_agent.invoke(
                    {
                        "messages": [
                            HumanMessage(
                                content=(
                                    "Review the Manim scene code that was just "
                                    "written. List the .py files in the workspace, "
                                    "read the scene file, and evaluate it against "
                                    "the description below.\n\n"
                                    "--- SCENE DESCRIPTION ---\n"
                                    f"{scene}\n"
                                    "--- END DESCRIPTION ---"
                                )
                            )
                        ]
                    }
                )
                all_messages += critic_result["messages"]

                if _is_approved(critic_result["messages"]):
                    print(
                        f"[CRITIC] Approved after {round_num + 1} review(s)"
                    )
                    break

                criticism = _extract_text(
                    critic_result["messages"][-1].content
                )
                print("[CRITIC] Revision requested")

                code_result = coding_agent.invoke(
                    {
                        "messages": [
                            HumanMessage(
                                content=(
                                    "Your Manim scene code has been reviewed "
                                    "and needs revision. Use list_files('.') to "
                                    "find the .py file, read it, apply the "
                                    "fixes, and write the updated version.\n\n"
                                    "--- ORIGINAL SCENE DESCRIPTION ---\n"
                                    f"{scene}\n"
                                    "--- END DESCRIPTION ---\n\n"
                                    "--- REVIEWER FEEDBACK ---\n"
                                    f"{criticism}\n"
                                    "--- END FEEDBACK ---"
                                )
                            )
                        ]
                    }
                )
                all_messages += code_result["messages"]

            # --- Step 3: Render the approved scene ---
            print("[RENDER] Rendering approved scene...")
            render_result = render_agent.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content=(
                                "A Manim scene has been written and approved. "
                                "Find the scene .py file in the workspace, "
                                "render it with manim, and use fetch_video to "
                                "deliver the output.\n\n"
                                "Scene description for reference:\n"
                                f"{scene}"
                            )
                        )
                    ]
                }
            )
            all_messages += render_result["messages"]

        return {"messages": all_messages}

    graph = StateGraph(MessagesState)

    graph.add_node("planner", planner_agent)
    graph.add_node("scene_runner", _run_scenes_sequentially)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "scene_runner")
    graph.add_edge("scene_runner", END)

    return graph.compile()
