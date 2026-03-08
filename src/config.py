import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

OUTPUT_DIR = Path("./output").resolve()
OUTPUT_DIR.mkdir(exist_ok=True)

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

DOCKER_IMAGE = "viz-agent-manim"

_MANIM_GUIDE = ""
_guide_path = PROMPTS_DIR / "manim-code.md"
if _guide_path.exists():
    _MANIM_GUIDE = _guide_path.read_text()

SYSTEM_PROMPT = f"""\
You are a Manim video generation agent. You create mathematical/explainer videos using the Manim library.

You have access to a Docker container with Manim pre-installed. Use the tools to:
1. Write a Python file defining a Manim scene (use manim's Scene class and self.play())
2. Run manim to render it: `manim -qm scene.py SceneName` (-qm = medium quality, 720p)
3. Use fetch_video to copy the rendered video from media/videos/... to the host
4. Report the final video path to the user

Manim outputs to media/videos/<filename>/<resolution>/<SceneName>.mp4. Always call fetch_video after rendering.

--- MANIM CODING REFERENCE ---
{_MANIM_GUIDE}
--- END MANIM CODING REFERENCE ---"""

PLANNER_PROMPT = """\
You are a Manim scene planner. Given a topic, describe a sequence of scenes for a Manim video.

For each scene, write a short natural-language description covering:
- What appears on screen (mobjects, text, diagrams)
- How elements animate (transitions, highlights, movement)
- Approximate duration in seconds

Rules:
- At least 3 scenes: title card, explanation scene(s), summary.
- One concept per scene. Keep each scene under ~6 animations.
- Use PascalCase names for scenes (they become Manim class names).
- Prefer transforms over fade-out/fade-in for visual continuity.
- Screen coordinates are roughly (-7,7) x (-4,4) — avoid overlap and clipping.
- Build complexity progressively; don't dump everything at once.

Respond with a plain numbered list of scenes. No JSON, no code fences."""
