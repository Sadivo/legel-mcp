from src.taiwan_law_mcp.server import search_judgments_by_law
import json

def test():
    print("Testing search_judgments_by_law ('勞動基準法 21')...")
    res1 = search_judgments_by_law("勞動基準法 21", max_results=3)
    print(json.dumps(json.loads(res1), indent=2, ensure_ascii=False))

    print("\nTesting search_judgments_by_law ('民法 184')...")
    res2 = search_judgments_by_law("民法 184", max_results=2)
    print(json.dumps(json.loads(res2), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test()
