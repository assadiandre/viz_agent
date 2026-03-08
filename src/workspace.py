import shutil
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parent.parent / ".workspace"


def create_workspace() -> Path:
    """Create a fresh workspace directory in the project root."""
    if WORKSPACE_DIR.exists():
        shutil.rmtree(WORKSPACE_DIR)
    WORKSPACE_DIR.mkdir()
    return WORKSPACE_DIR


def cleanup_workspace(workspace: Path) -> None:
    """Remove the workspace directory."""
    shutil.rmtree(workspace, ignore_errors=True)
