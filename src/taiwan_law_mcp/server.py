"""
台灣法規查詢 MCP 伺服器主程式（FastMCP 版）
"""

import json
from typing import Optional

from fastmcp import FastMCP

try:
    # 以套件模組執行時（uv run python -m taiwan_law_mcp）
    from .law_client import (
        search_law_by_name,
        get_law_pcode as _get_law_pcode,
        validate_pcode,
        fetch_law_by_pcode,
        parse_law_content,
        extract_law_meta,
        fetch_single_article,
        parse_single_article,
        keyword_search,
        _pick_parser,
    )
except ImportError:
    # 以獨立腳本或 fastmcp 直接指定檔案路徑執行時
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from law_client import (
        search_law_by_name,
        get_law_pcode as _get_law_pcode,
        validate_pcode,
        fetch_law_by_pcode,
        parse_law_content,
        extract_law_meta,
        fetch_single_article,
        parse_single_article,
        keyword_search,
        _pick_parser,
    )

from bs4 import BeautifulSoup


# === FastMCP 伺服器實例 ===
mcp = FastMCP(
    name="台灣法規查詢",
    instructions=(
        "這是台灣法規查詢系統，可以搜尋、查詢台灣法規條文。"
        "請用自然語言詢問法律問題，系統會自動選擇適合的工具查詢。"
    ),
)


@mcp.tool
def search_law(name: str, max_suggestions: int = 5) -> str:
    """搜尋台灣法規名稱，取得法規基本資訊和官方網址。
    
    當使用者想搜尋法規名稱、確認某法規是否存在，或是取得法規代碼(pcode)時使用此工具。
    
    Args:
        name: 法規名稱，例如：民法、刑法、財政收支劃分法
        max_suggestions: 搜尋結果最大建議數量（預設5）
    """
    result = search_law_by_name(name, max_suggestions)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
def get_law_pcode(name: str) -> str:
    """快速取得特定法規的專屬代碼(pcode)，供後續工具呼叫時使用。
    
    Args:
        name: 法規名稱，例如：民法
    """
    pcode = _get_law_pcode(name)
    result = {"name": name, "pcode": pcode, "found": pcode is not None}
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
def get_full_law(
    name: Optional[str] = None,
    pcode: Optional[str] = None,
    summary_mode: bool = False,
    max_articles: int = 0,
) -> str:
    """取得完整法規的所有條文內容。

    可接受法規名稱或法規代碼(pcode)作為輸入，提供pcode效率較高。
    支援摘要模式（每條只顯示第一行）以及設定條文數量上限，以控制 Token 消耗。

    Args:
        name: 法規名稱，例如：民法（與 pcode 二擇一）
        pcode: 法規代碼，例如：B0000001（優先於 name）
        summary_mode: 摘要模式，True=只顯示每條前一行（節省 Token），False=完整內容
        max_articles: 最大條文數量，0 表示無限制
    """
    if not pcode and name:
        search_result = search_law_by_name(name, max_suggestions=1)
        if search_result["status"] in ["exact_match", "single_match"]:
            pcode = search_result["result"]["pcode"]
        else:
            return json.dumps(
                {"error": "無法找到唯一匹配的法規", "suggestions": search_result.get("suggestions", [])},
                ensure_ascii=False, indent=2,
            )
    elif not pcode:
        return json.dumps({"error": "請提供法規名稱或pcode"}, ensure_ascii=False)

    html = fetch_law_by_pcode(pcode)
    soup = BeautifulSoup(html, _pick_parser())
    parsed = parse_law_content(html, summary_mode, max_articles)
    meta = extract_law_meta(soup)

    result = {
        "name": name or meta.get("name"),
        "pcode": pcode,
        "url": f"https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode={pcode}",
        "articles": parsed["flat_articles"],
        "structure": parsed["chapters"],
    }
    if "meta" in parsed:
        result["meta"] = parsed["meta"]

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
def get_single_article(
    article: str,
    name: Optional[str] = None,
    pcode: Optional[str] = None,
) -> str:
    """查詢特定法條的詳細內容（單條條文）。

    例如：查詢「民法第1條」、「刑法第271條」。
    提供 pcode 比提供 name 效率更高，可先用 get_law_pcode 取得。

    Args:
        article: 條文號碼，例如：1、16-1、271
        name: 法規名稱，例如：民法（與 pcode 二擇一）
        pcode: 法規代碼（優先於 name）
    """
    if not pcode and name:
        search_result = search_law_by_name(name, max_suggestions=1)
        if search_result["status"] in ["exact_match", "single_match"]:
            pcode = search_result["result"]["pcode"]
        else:
            return json.dumps(
                {"error": "無法找到唯一匹配的法規", "suggestions": search_result.get("suggestions", [])},
                ensure_ascii=False, indent=2,
            )
    elif not pcode:
        return json.dumps({"error": "請提供法規名稱或pcode"}, ensure_ascii=False)

    html = fetch_single_article(pcode, article)
    parsed = parse_single_article(html)

    result = {
        "pcode": pcode,
        "law_name": name,
        "url": f"https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode={pcode}&flno={article}",
        "article": parsed,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
def search_by_keyword(
    keyword: str,
    max_results: int = 10,
    summary_only: bool = True,
) -> str:
    """在全部台灣法規中以關鍵字搜尋相關條文。

    適合用於「找出所有提到某詞彙的法條」的情境，例如搜尋「安全無虞」、「契約」等關鍵字。

    Args:
        keyword: 搜尋關鍵字，例如：安全無虞、契約、責任
        max_results: 最大搜尋結果數量（預設10，設越大速度越慢）
        summary_only: True=只回傳匹配到的條文行（節省 Token），False=回傳完整條文
    """
    result = keyword_search(keyword, max_results, summary_only)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
def validate_law_pcode(pcode: str) -> str:
    """驗證法規代碼(pcode)是否為有效的台灣法規代碼。

    Args:
        pcode: 法規代碼，例如：B0000001
    """
    is_valid = validate_pcode(pcode)
    result = {"pcode": pcode, "valid": is_valid}
    return json.dumps(result, ensure_ascii=False, indent=2)


def main_sync():
    """同步版本的 main 函數，用於 CLI entry point"""
    mcp.run()


async def main():
    """非同步版本的 main 函數"""
    mcp.run()