import sys

from src.agent import build_agent
from src.stream_formatter import print_stream
from src.tools import init_tools
from src.workspace import create_workspace


def main():
    workspace = create_workspace()
    print(f"Workspace: {workspace}")

    tools = init_tools(workspace)
    agent = build_agent(tools)

    prompt = (
        sys.argv[1]
        if len(sys.argv) > 1 and sys.argv[1]
        else "Create a video explaining the pythagorean theorem."
    )

    stream = agent.stream(
        {"messages": [{"role": "user", "content": prompt}]},
        stream_mode="updates",
        subgraphs=True,
    )
    print_stream(stream)


if __name__ == "__main__":
    main()
