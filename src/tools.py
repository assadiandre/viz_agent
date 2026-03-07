import os

from langchain_core.tools import tool

from .config import OUTPUT_DIR
from .container import _workspace_path

_container = None


def init_tools(container):
    """Bind tools to a running Docker container and return the tool list."""
    global _container
    _container = container
    return [run_command, write_file, read_file, list_files, fetch_video]


@tool
def run_command(command: str) -> str:
    """Execute a shell command in the Docker container."""
    exit_code, output = _container.exec_run(cmd=["bash", "-c", command])
    return f"Exit code: {exit_code}\n{output.decode()}"


@tool
def write_file(path: str, content: str) -> str:
    """Write a file inside the Docker container. Path can be relative (e.g. 'scene.py') or absolute ('/workspace/scene.py')."""
    clean = _workspace_path(path)
    exit_code, output = _container.exec_run(
        cmd=["bash", "-c", f"cat > /workspace/{clean} << 'FILEEOF'\n{content}\nFILEEOF"]
    )
    return f"Wrote {clean}" if exit_code == 0 else f"Error: {output.decode()}"


@tool
def read_file(path: str) -> str:
    """Read a file from the Docker container. Path can be relative or absolute (/workspace/...)."""
    clean = _workspace_path(path)
    exit_code, output = _container.exec_run(cmd=["cat", f"/workspace/{clean}"])
    return output.decode() if exit_code == 0 else f"Error: {output.decode()}"


@tool
def list_files(path: str = ".") -> str:
    """List files in a directory inside the Docker container. Path can be relative or absolute (/workspace/...)."""
    clean = _workspace_path(path)
    exit_code, output = _container.exec_run(cmd=["ls", "-la", f"/workspace/{clean}"])
    return output.decode()


@tool
def fetch_video(container_path: str) -> str:
    """Copy a video file from the container to the host output directory.
    Pass the path in the container, e.g. 'media/videos/scene/1080p60/Scene.mp4'
    (relative to /workspace) or '/tmp/media/videos/...' (absolute).
    Returns the absolute path to the video on the host."""
    clean = _workspace_path(container_path)
    filename = os.path.basename(clean)
    if container_path.startswith("/") and not container_path.startswith("/workspace"):
        src = container_path
    else:
        src = f"/workspace/{clean}"
    dst = f"/output/{filename}"
    exit_code, output = _container.exec_run(cmd=["cp", src, dst])
    if exit_code != 0:
        return f"Error copying video: {output.decode()}"
    host_path = OUTPUT_DIR / filename
    return str(host_path)
