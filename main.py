import sys

from src.agent import build_agent
from src.container import create_container
from src.stream_formatter import print_stream
from src.tools import init_tools


def main():
    container = create_container()
    try:
        tools = init_tools(container)
        agent = build_agent(tools)

        prompt = (
            sys.argv[1]
            if len(sys.argv) > 1 and sys.argv[1]
            else "Create a video explaining the pythagorean theorem."
        )

        stream = agent.stream(
            {"messages": [{"role": "user", "content": prompt}]},
            stream_mode="values",
        )
        print_stream(stream)
    finally:
        container.stop()
        container.remove()


if __name__ == "__main__":
    main()
