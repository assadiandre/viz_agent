import os
import shutil
import subprocess
from pathlib import Path

from langchain_core.tools import tool

from .config import OUTPUT_DIR

_workspace: Path | None = None


def init_tools(workspace: Path):
    """Bind tools to a workspace directory and return the tool list."""
    global _workspace
    _workspace = workspace
    return [run_command, write_file, read_file, list_files, fetch_video]


@tool
def run_command(command: str) -> str:
    """Execute a shell command inside the workspace directory."""
    result = subprocess.run(
        ["bash", "-c", command],
        cwd=str(_workspace),
        capture_output=True,
        text=True,
        timeout=300,
    )
    output = (result.stdout + result.stderr).strip()
    return f"Exit code: {result.returncode}\n{output}"


@tool
def write_file(path: str, content: str) -> str:
    """Write a file inside the workspace. Path is relative to the workspace root."""
    target = _workspace / path.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return f"Wrote {path}"


@tool
def read_file(path: str) -> str:
    """Read a file from the workspace. Path is relative to the workspace root."""
    target = _workspace / path.lstrip("/")
    if not target.exists():
        return f"Error: {path} not found"
    return target.read_text()


@tool
def list_files(path: str = ".") -> str:
    """List files in a directory inside the workspace."""
    target = _workspace / path.lstrip("/")
    if not target.exists():
        return f"Error: {path} not found"
    result = subprocess.run(
        ["ls", "-la", str(target)],
        capture_output=True,
        text=True,
    )
    return result.stdout


@tool
def fetch_video(file_path: str) -> str:
    """Copy a rendered video from the workspace to the output directory.
    Pass the path relative to the workspace, e.g. 'media/videos/scene/1080p60/Scene.mp4'.
    Returns the absolute path to the video on the host."""
    src = _workspace / file_path.lstrip("/")
    if not src.exists():
        return f"Error: {file_path} not found in workspace"
    filename = src.name
    dst = OUTPUT_DIR / filename
    shutil.copy2(str(src), str(dst))
    return str(dst)
