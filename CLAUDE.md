# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Taiwan Law MCP server built with **FastMCP** framework. Interfaces with Taiwan's Ministry of Justice legal database (`https://law.moj.gov.tw/`) to provide law search and retrieval tools.

## Development Commands

```bash
# Install dependencies (Python 3.10+ required)
uv sync

# Start MCP server (FastMCP CLI)
uv run fastmcp run src/taiwan_law_mcp/server.py

# Inspect server tools (verify setup)
uv run fastmcp inspect src/taiwan_law_mcp/server.py

# Install as CLI tool
taiwan-law-mcp
```

## Architecture

```
src/taiwan_law_mcp/
├── server.py       # FastMCP server — 6 @mcp.tool decorated functions
├── law_client.py   # Core scraping logic — requests + BeautifulSoup
├── __init__.py
└── __main__.py

archive/            # Legacy files (old mcp SDK servers, test scripts)
```

### Key Components

1. **`server.py`** — FastMCP server, defines 6 tools via `@mcp.tool` decorator. Automatically generates JSON schema from Python type annotations and docstrings.

2. **`law_client.py`** — Standalone scraping library. Can be used without MCP. Handles:
   - ASP.NET form state (`__VIEWSTATE`) for search submissions
   - HTML parsing of law content (chapters, articles, lines)
   - Session management and proper headers

### The 6 MCP Tools

| Tool | Function |
|---|---|
| `search_law(name, max_suggestions=5)` | Search by law name |
| `get_law_pcode(name)` | Get law code (pcode) |
| `get_full_law(name, pcode, summary_mode, max_articles)` | Full law content |
| `get_single_article(article, name, pcode)` | Single article lookup |
| `search_by_keyword(keyword, max_results, summary_only)` | Keyword search |
| `validate_law_pcode(pcode)` | Validate pcode |

### Import Pattern

`server.py` uses a try/except import to support both package module and direct file execution:

```python
try:
    from .law_client import ...   # Package mode
except ImportError:
    from law_client import ...    # Direct file mode (fastmcp run file.py)
```

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "taiwan-law": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/legel-mcp",
               "fastmcp", "run", "src/taiwan_law_mcp/server.py"]
    }
  }
}
```

## Notes

- All law data is fetched live from `law.moj.gov.tw` — requires internet
- On Windows: `lxml` is not available, falls back to `html.parser` automatically
- `summary_mode=True` on `get_full_law` returns only the first line of each article (reduces token usage significantly)