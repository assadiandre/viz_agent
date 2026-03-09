import math
import shutil
import subprocess
from pathlib import Path

from langchain_core.tools import tool

from .config import OUTPUT_DIR

_workspace: Path | None = None

_CALC_SAFE = {
    # Trig
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "atan2": math.atan2,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "asinh": math.asinh,
    "acosh": math.acosh,
    "atanh": math.atanh,
    "degrees": math.degrees,
    "radians": math.radians,
    # Powers / roots / logs
    "sqrt": math.sqrt,
    "pow": pow,
    "log": math.log,
    "log2": math.log2,
    "log10": math.log10,
    "exp": math.exp,
    # Rounding / sign
    "abs": abs,
    "round": round,
    "ceil": math.ceil,
    "floor": math.floor,
    "trunc": math.trunc,
    "copysign": math.copysign,
    # Aggregates
    "min": min,
    "max": max,
    "sum": sum,
    # Combinatorics
    "factorial": math.factorial,
    "comb": math.comb,
    "perm": math.perm,
    "gcd": math.gcd,
    "lcm": math.lcm,
    # Geometry / misc
    "hypot": math.hypot,
    "dist": math.dist,
    "fmod": math.fmod,
    "remainder": math.remainder,
    "isclose": math.isclose,
    # Constants
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "inf": math.inf,
}


def init_tools(workspace: Path):
    """Bind tools to a workspace directory and return the tool list."""
    global _workspace
    _workspace = workspace
    return [
        run_command,
        write_file,
        read_file,
        list_files,
        fetch_video,
        calculator,
    ]


def get_coding_tools():
    """Tools for the coding agent: write, read, list, calculate."""
    return [write_file, read_file, list_files, calculator]


def get_critic_tools():
    """Tools for the critic agent: read, list, calculate."""
    return [read_file, list_files, calculator]


def get_render_tools():
    """Tools for the render agent: run commands, read, list, fetch video."""
    return [run_command, read_file, list_files, fetch_video]


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
    if target.is_dir():
        return f"Error: {path} is a directory, not a file. Use list_files to browse directories."
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
def calculator(expression: str) -> str:
    """Evaluate a math expression for positioning calculations.
    Supports: +, -, *, /, **,
      trig: sin, cos, tan, asin, acos, atan, atan2, sinh, cosh, tanh, asinh, acosh, atanh, degrees, radians,
      powers/logs: sqrt, pow, log, log2, log10, exp,
      rounding: abs, round, ceil, floor, trunc,
      aggregates: min, max, sum,
      combinatorics: factorial, comb, perm, gcd, lcm,
      geometry: hypot, dist, fmod, remainder, isclose,
      constants: pi, e, tau, inf.
    Examples: 'atan2(3, 4)', 'degrees(pi/6)' -> 30.0, 'hypot(3, 4)' -> 5.0"""
    try:
        result = eval(expression, {"__builtins__": {}}, _CALC_SAFE)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


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
