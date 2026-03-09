from langchain_core.messages.utils import AnyMessage


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
    GOOGLE_API_KEY,
    HARDCODED_PLAN,
    OPENAI_API_KEY,
    PLANNER_PROMPT_V3,
    SYSTEM_PROMPT,
)


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


def build_agent(tools, *, llm=None):
    """Create a StateGraph: planner -> one primary_agent per scene (sequential)."""

    # Hardcode this for now (for testing)
    def planner_agent(state: MessagesState) -> MessagesState:
        return {"messages": state["messages"] + [AIMessage(content=HARDCODED_PLAN)]}

    primary_agent = _build_llm_agent(tools, llm=llm_openai, system_prompt=CODING_PROMPT)

    def _run_scenes_sequentially(state: MessagesState) -> MessagesState:
        planner_text = _extract_text(state["messages"][-1].content)
        scenes = _parse_scenes(planner_text)
        all_messages = list(state["messages"])

        print("SCENE LENGTH: ", len(scenes))

        for scene in scenes:
            result = primary_agent.invoke(
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
            all_messages = all_messages + result["messages"]

        return {"messages": all_messages}

    graph = StateGraph(MessagesState)

    graph.add_node("planner", planner_agent)
    graph.add_node("scene_runner", _run_scenes_sequentially)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "scene_runner")
    graph.add_edge("scene_runner", END)

    return graph.compile()
