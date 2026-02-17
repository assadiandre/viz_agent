"""Format agent stream output for readable CLI display."""

from langchain_core.messages import AIMessage, ToolMessage


def format_ai_content(content) -> str:
    """Extract readable text from AI message content (handles str or content blocks)."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text" and "text" in block:
                    parts.append(block["text"])
            elif hasattr(block, "text"):
                parts.append(block.text)
        return "\n".join(parts).strip() if parts else ""
    return str(content)


def format_tool_call(name: str, args: dict) -> str:
    """Summarize a tool call for display (avoid dumping huge content)."""
    if name == "write_file":
        path = args.get("path", "?")
        content_len = len(args.get("content", ""))
        return f"write_file path={path!r} ({content_len} chars)"
    if name == "run_command":
        cmd = args.get("command", "")
        first_line = cmd.split("\n")[0] if "\n" in cmd else cmd
        if len(first_line) > 60:
            first_line = first_line[:57] + "..."
        suffix = " (multi-line)" if "\n" in cmd else ""
        return f"run_command {first_line!r}{suffix}"
    if name == "read_file":
        return f"read_file path={args.get('path', '?')!r}"
    if name == "list_files":
        return f"list_files path={args.get('path', '.')!r}"
    if name == "fetch_video":
        return f"fetch_video path={args.get('container_path', '?')!r}"
    return f"{name}({args})"


def format_tool_result(content: str, max_len: int = 300) -> str:
    """Truncate and indent tool output for readability."""
    content = content.strip()
    if len(content) > max_len:
        content = content[:max_len] + "\n... (truncated)"
    if "\n" in content:
        return "\n" + "\n".join("  " + line for line in content.splitlines())
    return " " + content


def print_stream(stream, *, header: str = "--- Streaming steps ---"):
    """Consume an agent stream and print formatted output to stdout."""
    print(f"{header}\n")
    seen_count = 0

    for chunk in stream:
        messages = chunk.get("messages", [])
        for msg in messages[seen_count:]:
            if isinstance(msg, AIMessage):
                text = format_ai_content(msg.content)
                if text:
                    print(f"🤖 {text}\n")
                if msg.tool_calls:
                    for tc in msg.tool_calls:
                        name = tc.get("name", "?")
                        args = tc.get("args", {})
                        print(f"  ⚡ {format_tool_call(name, args)}\n")
            elif isinstance(msg, ToolMessage):
                content = format_tool_result(msg.content)
                print(f"  ✓ [{msg.name}]{content}\n")
            seen_count += 1
