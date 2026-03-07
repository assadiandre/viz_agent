from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from .config import ANTHROPIC_API_KEY, OPENAI_API_KEY, SYSTEM_PROMPT


llm_anthropic = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=ANTHROPIC_API_KEY,
)

llm_openai = ChatOpenAI(
    model="gpt-5.3-codex",
    api_key=OPENAI_API_KEY,
)


def build_agent(tools, *, llm=None):
    """Create a LangGraph agent wired to the given tools."""
    return create_agent(
        model=llm or llm_openai,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
