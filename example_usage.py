"""Example usage for Semantic Cache & Prompt Deduplication Sentinel."""
from client import SemanticCacheSentinel

if __name__ == "__main__":
    cache = [
        {"prompt": "Analyze Q3 revenue and EBITDA growth numbers", "response": "Revenue was up 18% YoY with EBITDA margin at 24%.", "cached_at": 1000000000.0, "ttl_seconds": 9999999999}
    ]
    res = SemanticCacheSentinel.lookup_cache("Please analyze Q3 revenue and EBITDA growth figures", cache, similarity_threshold=0.7)
    print("Cache Lookup Result:", res)
