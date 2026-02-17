.PHONY: install build run clean

install:
	uv sync

build:
	docker build -t viz-agent-manim .

# Usage: make run  (uses default prompt) or make run PROMPT="Your video description"
run:
	uv run python main.py "$(PROMPT)"

clean:
	-docker stop $$(docker ps -q --filter ancestor=viz-agent-manim) 2>/dev/null || true
