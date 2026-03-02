# Taiwan Law MCP 台灣法規查詢 MCP 伺服器

基於 **FastMCP** 框架開發的台灣法規查詢系統，提供簡潔、高效的法規搜尋和條文查詢功能。

## 特色功能

- 🚀 **FastMCP 框架** - 採用官方推薦的高階 MCP 框架，程式碼簡潔易維護
- 📉 **Token 耗用優化** - 摘要模式、條文分頁、關鍵字精準回傳
- 🔍 **6 種查詢工具** - 涵蓋搜尋、條文、關鍵字、代碼驗證等場景
- 🌐 **資料來源** - 直連 [法務部全國法規資料庫](https://law.moj.gov.tw/)

## 主要工具

| 工具 | 說明 |
|---|---|
| `search_law` | 搜尋法規名稱，取得基本資訊與官方連結 |
| `get_law_pcode` | 快速取得法規代碼（pcode），供後續工具使用 |
| `get_full_law` | 取得完整法規條文，支援**摘要模式**與條文數量限制 |
| `get_single_article` | 查詢特定法條詳細內容（例如：民法第1條）|
| `search_by_keyword` | 在所有法規中以關鍵字搜尋相關條文 |
| `validate_law_pcode` | 驗證法規代碼（pcode）是否有效 |

## 安裝使用

### 使用 UVX（推薦，無需安裝）

```bash
uvx taiwan-law-mcp
```

### 使用 pip

```bash
pip install taiwan-law-mcp
taiwan-law-mcp
```

### 本地開發

```bash
git clone <repository-url>
cd legel-mcp

# 安裝依賴（需要 Python 3.10+）
uv sync

# 啟動伺服器
uv run fastmcp run src/taiwan_law_mcp/server.py
```

## Claude Desktop 設定

### 方法一：uvx（最簡單）

```json
{
  "mcpServers": {
    "taiwan-law": {
      "command": "uvx",
      "args": ["taiwan-law-mcp"]
    }
  }
}
```

### 方法二：本地開發模式

```json
{
  "mcpServers": {
    "taiwan-law": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "C:/path/to/legel-mcp",
        "fastmcp", "run", "src/taiwan_law_mcp/server.py"
      ]
    }
  }
}
```

**設定檔位置：**
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

## 使用範例

不需要特殊指令，用自然語言詢問即可：

- 「我想了解民法第 1 條」
- 「搜尋包含契約的法條」
- 「公司設立需要什麼條件？」
- 「查詢公平交易法的獨占規定」

## API 範例

### 搜尋法規

```json
{
  "name": "search_law",
  "arguments": { "name": "公平交易法" }
}
```

### 取得完整法規（摘要模式）

```json
{
  "name": "get_full_law",
  "arguments": {
    "pcode": "J0150002",
    "summary_mode": true,
    "max_articles": 20
  }
}
```

### 關鍵字搜尋

```json
{
  "name": "search_by_keyword",
  "arguments": {
    "keyword": "獨占",
    "max_results": 10,
    "summary_only": true
  }
}
```

## 技術規格

- **Python 版本**: 3.10+
- **框架**: [FastMCP](https://gofastmcp.com/) 3.x
- **主要依賴**:
  - `fastmcp >= 2.0.0`
  - `requests >= 2.28.0`
  - `beautifulsoup4 >= 4.11.0`

## 開發

```bash
# 安裝含開發工具的環境
uv sync --dev

# 驗證伺服器設定
uv run fastmcp inspect src/taiwan_law_mcp/server.py

# 程式碼格式化
uv run black src
uv run ruff check src
```

---

## ⚠️ 免責聲明

本工具僅提供法條查詢功能，**不提供法律建議**。如需專業法律意見，請諮詢合格律師或相關專業人士。

---

## 📚 參考來源

本專案基於以下開源專案進行修改與改良：

- **原始專案**：[wasonisgood/legel-mcp](https://github.com/wasonisgood/legel-mcp)
- **主要改動**：
  - 將 MCP 伺服器從低階 `mcp` SDK 遷移至 [FastMCP](https://gofastmcp.com/) 框架
  - 整理並移除冗餘的多版本 server 執行檔
  - 更新套件依賴、Python 最低版本要求與專案設定

- **資料來源**：[法務部全國法規資料庫](https://law.moj.gov.tw/)

---
