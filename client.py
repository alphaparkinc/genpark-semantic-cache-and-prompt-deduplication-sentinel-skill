"""Semantic Cache & Prompt Deduplication Sentinel.
100% Python Standard Library.
"""

import time
import re

class SemanticCacheSentinel:
    """Evaluates prompt similarity via n-gram shingling and token hashing to serve cached agent responses."""

    @staticmethod
    def _shingle_tokens(text: str, n: int = 3) -> set:
        words = re.findall(r"\w+", text.lower())
        if len(words) < n:
            return {" ".join(words)}
        return {" ".join(words[i:i+n]) for i in range(len(words) - n + 1)}

    @classmethod
    def calculate_similarity(cls, prompt_a: str, prompt_b: str) -> float:
        s_a = cls._shingle_tokens(prompt_a)
        s_b = cls._shingle_tokens(prompt_b)
        intersection = len(s_a.intersection(s_b))
        union = len(s_a.union(s_b))
        return intersection / union if union > 0 else 0.0

    @classmethod
    def lookup_cache(cls, incoming_prompt: str, cache_entries: list, similarity_threshold: float = 0.8) -> dict:
        best_match = None
        highest_sim = 0.0

        for entry in cache_entries:
            cached_prompt = entry.get("prompt", "")
            cached_response = entry.get("response", "")
            cached_at = float(entry.get("cached_at", 0))
            ttl_seconds = float(entry.get("ttl_seconds", 3600))

            if time.time() - cached_at > ttl_seconds:
                continue

            sim = cls.calculate_similarity(incoming_prompt, cached_prompt)
            if sim > highest_sim:
                highest_sim = sim
                if sim >= similarity_threshold:
                    best_match = entry

        if best_match and highest_sim >= similarity_threshold:
            return {
                "cache_status": "HIT",
                "similarity_score": round(highest_sim, 3),
                "matched_prompt": best_match.get("prompt"),
                "cached_response": best_match.get("response"),
                "token_savings_pct": 100.0
            }

        return {
            "cache_status": "MISS",
            "similarity_score": round(highest_sim, 3),
            "recommendation": "EXECUTE_MODEL_CALL_AND_STORE"
        }
