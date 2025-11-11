import re
import os
import json
from datetime import datetime
from typing import Callable, Dict, Any, Optional

MEMORY_PATH = "memory.json"


class Session:
    def __init__(self):
        self.user_name: Optional[str] = None
        self.last_intent: Optional[str] = None
        self.turns = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_name": self.user_name,
            "last_intent": self.last_intent,
            "turns": self.turns
        }

    @classmethod
    def from_dict(cls, d):
        session = cls()
        session.user_name = d.get("user_name")
        session.last_intent = d.get("last_intent")
        session.turns = d.get("turns", 0)
        return session


def load_memory() -> Session:
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            data = json.load(f)
            return Session.from_dict(data)
    else:
        return Session()


def save_memory(session: Session):
    with open(MEMORY_PATH, "w") as f:
        json.dump(session.to_dict(), f)


Pattern = re.Pattern[str]
Handler = Callable[[Session, Dict[str, Any]], str]


class Router:
    def __init__(self):
        self.routes: list[tuple[Pattern, str, Handler]] = []

    def add(self, pattern: str, intent: str, handler: Handler):
        self.routes.append((re.compile(pattern, re.I), intent, handler))

    def match(self, text: str):
        for pattern, intent, handler in self.routes:
            m = pattern.search(text)
            if m:
                return intent, handler, m.groupdict()
        return None, None, {}


router = Router()


def handle_greet(s: Session, _: Dict[str, Any]) -> str:
    if s.user_name:
        return f'Hello {s.user_name}! How can I help you today?'
    else:
        return "Hello! What's your name?"


router.add(r'\b(hi|hello|hey|buenos dias)\b', "greet", handle_greet)


def reply(s: Session, text: str) -> str:
    s.turns += 1
    text = text.strip()
    i, h, d = router.match(text)
    if h:
        return h(s, d)
    else:
        return "I didn't catch that. Can you rephrase?"


def main():
    session = load_memory()
    user = input("> ")
    bot = reply(session, user)
    print(bot)


if __name__ == "__main__":
    main()
