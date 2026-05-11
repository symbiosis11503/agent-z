"""Ch 6 — 你的第一個 MCP server

3 個 tools:
  - count_lines: 數一個檔案有幾行
  - search_in_file: 在檔案裡 grep
  - list_files: 列一個資料夾

跑：
    uv run server.py                 # stdio mode, Claude Code 接這個
    或
    uv pip install mcp
    python server.py

接 Claude Code (mac/linux):
    將下面塊加到 ~/.config/claude/claude.json (見 README §3):

    {
      "mcpServers": {
        "agentz-demo": {
          "command": "/path/to/.venv/bin/python",
          "args": ["/path/to/this/server.py"]
        }
      }
    }
"""
from __future__ import annotations

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("agentz-demo")


@mcp.tool()
def count_lines(file_path: str) -> dict:
    """數一個檔案有幾行（純文字檔）。

    Args:
        file_path: 絕對路徑或相對路徑。

    Returns:
        dict with file_path, line_count, bytes.
    """
    p = Path(file_path).expanduser().resolve()
    if not p.exists():
        return {"error": f"file not found: {p}"}
    if not p.is_file():
        return {"error": f"not a file: {p}"}
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": f"read fail: {e}"}
    return {
        "file_path": str(p),
        "line_count": text.count("\n") + (1 if text and not text.endswith("\n") else 0),
        "bytes": p.stat().st_size,
    }


@mcp.tool()
def search_in_file(file_path: str, query: str, max_matches: int = 10) -> dict:
    """在檔案裡找 query 字串，回傳每個 hit 的 line number + 內容。

    Args:
        file_path: 檔案路徑
        query: 要找的字串（case-sensitive）
        max_matches: 最多回傳幾個（防爆）

    Returns:
        dict with matches list.
    """
    p = Path(file_path).expanduser().resolve()
    if not p.exists() or not p.is_file():
        return {"error": f"file not found: {p}"}
    matches = []
    try:
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if query in line:
                matches.append({"line": i, "content": line.strip()[:200]})
                if len(matches) >= max_matches:
                    break
    except Exception as e:
        return {"error": f"read fail: {e}"}
    return {
        "file_path": str(p),
        "query": query,
        "match_count": len(matches),
        "matches": matches,
        "truncated": len(matches) >= max_matches,
    }


@mcp.tool()
def list_files(dir_path: str = ".", pattern: str = "*") -> dict:
    """列一個資料夾的檔案（不遞迴）。

    Args:
        dir_path: 資料夾路徑（預設 cwd）
        pattern: glob pattern (e.g. "*.py", "*.md")

    Returns:
        dict with files list (max 100, 防爆).
    """
    p = Path(dir_path).expanduser().resolve()
    if not p.exists() or not p.is_dir():
        return {"error": f"not a dir: {p}"}
    files = []
    for f in sorted(p.glob(pattern))[:100]:
        files.append({
            "name": f.name,
            "type": "dir" if f.is_dir() else "file",
            "size": f.stat().st_size if f.is_file() else None,
        })
    return {"dir": str(p), "pattern": pattern, "count": len(files), "files": files}


def main():
    """Entry point — Claude Code 用 stdio 跑這個。"""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
