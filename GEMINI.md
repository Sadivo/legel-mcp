# Taiwan Law MCP 專案規範與指南 (GEMINI.md)

本文件為 Gemini CLI 提供關於 **Taiwan Law MCP (台灣法規查詢伺服器)** 專案的上下文與指令規範。

## 1. 專案概述
- **目標**：基於 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 建立的台灣法律查詢伺服器。
- **核心框架**：[FastMCP](https://gofastmcp.com/) (Python)。
- **資料來源**：[法務部全國法規資料庫](https://law.moj.gov.tw/)。
- **技術棧**：Python 3.10+, `uv`, `fastmcp`, `requests`, `beautifulsoup4`。

## 2. 目錄結構
- `src/taiwan_law_mcp/`：核心程式碼。
  - `server.py`：MCP 伺服器定義，包含工具 (@mcp.tool) 聲明。
  - `law_client.py`：網頁爬蟲邏輯，負責與法務部資料庫互動。
  - `__main__.py`：套件執行進入點。
- `archive/`：舊版或備份程式碼，非正式執行路徑。
- `script/`：輔助工具腳本，用於資料處理或關鍵字搜尋測試。
- `pyproject.toml`：專案配置與依賴定義。

## 3. 開發與執行指令
專案統一使用 `uv` 進行管理，**禁止在全域環境執行程式**。

### 環境準備
```bash
# 安裝依賴並建立虛擬環境
uv sync
```

### 啟動伺服器
```bash
# 使用 fastmcp 開發模式啟動
uv run fastmcp run src/taiwan_law_mcp/server.py

# 使用 dev 模式（具備熱重載功能）
uv run fastmcp dev src/taiwan_law_mcp/server.py
```

### 工具驗證與測試
```bash
# 檢查 MCP 工具定義是否正確
uv run fastmcp inspect src/taiwan_law_mcp/server.py

# 執行測試（若有 tests 目錄）
uv run pytest
```

### 程式碼規範
```bash
# 格式化代碼
uv run black src
# 靜態檢查
uv run ruff check src
```

## 4. MCP 工具說明
本伺服器提供以下 6 個核心工具：
1. `search_law`：搜尋法規名稱與基本資訊。
2. `get_law_pcode`：取得法規專屬代碼 (PCode)。
3. `get_full_law`：取得完整條文（支援摘要模式以節省 Token）。
4. `get_single_article`：精準查詢特定法條（如：民法第1條）。
5. `search_by_keyword`：跨法規關鍵字搜尋。
6. `validate_law_pcode`：驗證 PCode 有效性。

## 5. 開發慣例與注意事項
- **Windows 相容性**：由於 Windows 上 `lxml` 可能安裝失敗，系統會自動回退使用 `html.parser`。
- **Token 優化**：
  - 優先推薦使用者使用 `summary_mode=True` 進行初步瀏覽。
  - 條文過多時應使用 `max_articles` 限制回傳量。
- **網路依賴**：所有資料皆為即時抓取，執行時需確保網路連線。
- **錯誤處理**：`law_client.py` 處理了 ASP.NET 的 `__VIEWSTATE` 狀態，修改爬蟲邏輯時需特別注意請求標頭 (Headers)。
- **匯入路徑**：`server.py` 採用 `try-except` 兼顧「套件執行」與「直接執行檔案」的匯入路徑。

## 6. 專案環境要求 (系統強制規範複述)
- 執行 Python 程式前必須先檢查或建立 `venv`。
- 安裝套件與環境管理一律使用 `uv`。
- 所有回覆與文件產出預設使用**繁體中文**。
