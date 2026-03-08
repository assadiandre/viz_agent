from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph

from .config import ANTHROPIC_API_KEY, OPENAI_API_KEY, PLANNER_PROMPT, SYSTEM_PROMPT


llm_anthropic = ChatAnthropic(
    model="claude-opus-4-6",
    api_key=ANTHROPIC_API_KEY,
)

llm_openai = ChatOpenAI(
    model="gpt-5.3-codex",
    api_key=OPENAI_API_KEY,
)


def _build_llm_agent(tools, *, llm=None, system_prompt=SYSTEM_PROMPT):
    """Create one LangChain agent node."""
    return create_agent(
        model=llm or llm_openai,
        tools=tools,
        system_prompt=system_prompt,
    )


def build_agent(tools, *, llm=None):
    """Create a 3-agent StateGraph: planner -> primary agent -> reviewer agent."""
    planner_agent = _build_llm_agent([], llm=llm, system_prompt=PLANNER_PROMPT)
    primary_agent = _build_llm_agent(tools, llm=llm, system_prompt=SYSTEM_PROMPT)
    reviewer_agent = _build_llm_agent(
        tools,
        llm=llm,
        system_prompt=(
            "You are a second-pass assistant. Review the previous agent output. "
            "Answer the question: is this video satisfactory? If yes, return 'APPROVED'. "
            "If no, return 'REJECTED'. Explain your reasoning."
        ),
    )

    graph = StateGraph(MessagesState)

    graph.add_node("planner", planner_agent)
    graph.add_node("primary_agent", primary_agent)
    graph.add_node("reviewer_agent", reviewer_agent)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "primary_agent")
    graph.add_edge("primary_agent", "reviewer_agent")
    graph.add_edge("reviewer_agent", END)
    return graph.compile()
