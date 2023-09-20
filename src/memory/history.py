from typing import Dict, List

class History:
    """A class for maintaining the history of a conversation."""

    def __init__(self, sys: str) -> None:
        self.history = [{"role": "system", "content": sys}]

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_last(self, n: int) -> List[Dict[str, str]]:
        return self.history[-n:]

    def get_full_history(self) -> List[Dict[str, str]]:
        return self.history
