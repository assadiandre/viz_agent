FROM manimcommunity/manim:latest

WORKDIR /workspace

# Keep container alive for agent to exec into
CMD ["sleep", "infinity"]
