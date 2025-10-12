# utils.py

# Very simple keyword-based crisis detection placeholder.
# Replace with a robust classifier later.
from typing import List
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "i want to die", "hurt myself",
    "can't go on", "kill myself", "hang myself"
]

def detect_crisis(text: str) -> bool:
    if not text:
        return False
    s = text.lower()
    for kw in CRISIS_KEYWORDS:
        if kw in s:
            return True
    return False
