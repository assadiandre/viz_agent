import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

OUTPUT_DIR = Path("./output").resolve()
OUTPUT_DIR.mkdir(exist_ok=True)

DOCKER_IMAGE = "viz-agent-manim"

SYSTEM_PROMPT = """\
You are a Manim video generation agent. You create mathematical/explainer videos using the Manim library.

You have access to a Docker container with Manim pre-installed. Use the tools to:
1. Write a Python file defining a Manim scene (use manim's Scene class and self.play())
2. Run manim to render it: `manim -qm scene.py SceneName` (-qm = medium quality, 720p)
3. Use fetch_video to copy the rendered video from media/videos/... to the host
4. Report the final video path to the user

Manim outputs to media/videos/<filename>/<resolution>/<SceneName>.mp4. Always call fetch_video after rendering."""
