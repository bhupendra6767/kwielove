"""
responder.py — Loads triggers/responses and matches messages using fuzzy matching.
"""

import json
import random
import re
from rapidfuzz import process, fuzz
from config import FUZZY_THRESHOLD, TRIGGERS_PATH, RESPONSES_PATH


class Responder:
    def __init__(self):
        self.triggers: dict[str, str] = {}   # trigger_text → category
        self.responses: dict[str, list[str]] = {}  # category → [responses]
        self._trigger_keys: list[str] = []

    def load(self):
        with open(TRIGGERS_PATH, encoding="utf-8") as f:
            self.triggers = json.load(f)
        with open(RESPONSES_PATH, encoding="utf-8") as f:
            self.responses = json.load(f)
        self._trigger_keys = list(self.triggers.keys())

    @property
    def trigger_count(self) -> int:
        return len(self.triggers)

    @property
    def response_count(self) -> int:
        return sum(len(v) for v in self.responses.values())

    def _clean(self, text: str) -> str:
        """Lowercase and strip punctuation/extra spaces from a message."""
        text = text.lower().strip()
        # Remove leading punctuation but keep emojis
        text = re.sub(r"^[^\w\U00010000-\U0010ffff]+", "", text, flags=re.UNICODE)
        text = re.sub(r"\s+", " ", text)
        return text

    def get_response(self, message: str) -> str | None:
        """
        Try to find a matching trigger for the message.
        Returns a random response string, or None if no match found.
        """
        cleaned = self._clean(message)
        if not cleaned:
            return None

        # 1. Exact match
        if cleaned in self.triggers:
            category = self.triggers[cleaned]
            return self._pick_response(category)

        # 2. Fuzzy match against all trigger keys
        result = process.extractOne(
            cleaned,
            self._trigger_keys,
            scorer=fuzz.token_sort_ratio,
            score_cutoff=FUZZY_THRESHOLD,
        )
        if result:
            matched_trigger, score, _ = result
            category = self.triggers[matched_trigger]
            return self._pick_response(category)

        # 3. Check if any trigger is contained in the message
        for trigger, category in self.triggers.items():
            if trigger in cleaned:
                return self._pick_response(category)

        return None

    def _pick_response(self, category: str) -> str:
        pool = self.responses.get(category) or self.responses.get("default", [])
        if not pool:
            return "👋"
        return random.choice(pool)
