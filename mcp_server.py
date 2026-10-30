"""MCP server for Semantic Cache & Prompt Deduplication Sentinel."""
import sys
import json
from client import SemanticCacheSentinel

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "lookup_cache",
                    "description": "Evaluate prompt similarity against cached responses to avoid redundant LLM calls",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "incoming_prompt": {"type": "string"},
                            "cache_entries": {"type": "array"},
                            "similarity_threshold": {"type": "number", "default": 0.8}
                        },
                        "required": ["incoming_prompt", "cache_entries"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "lookup_cache":
            out = SemanticCacheSentinel.lookup_cache(
                args.get("incoming_prompt", ""),
                args.get("cache_entries", []),
                float(args.get("similarity_threshold", 0.8))
            )
            return {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}
    return {"error": "Unsupported method or tool"}

if __name__ == "__main__":
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()
