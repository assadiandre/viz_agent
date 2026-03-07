import docker

from .config import DOCKER_IMAGE, OUTPUT_DIR


def _workspace_path(path: str) -> str:
    """Normalize path to be relative to /workspace (avoids double /workspace/)."""
    p = path.lstrip("/").replace("/workspace/", "").replace("workspace/", "")
    return p or "."


def create_container():
    """Spin up a detached Manim container with workspace + output volumes."""
    client = docker.from_env()
    return client.containers.run(
        DOCKER_IMAGE,
        detach=True,
        user="root",
        working_dir="/workspace",
        volumes={
            "agent_workspace": {"bind": "/workspace", "mode": "rw"},
            str(OUTPUT_DIR): {"bind": "/output", "mode": "rw"},
        },
    )
