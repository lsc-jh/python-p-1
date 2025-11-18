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


def intent(pattern: str, name: str):
    def deco(fn):
        router.add(pattern, name, fn)
        return fn

    return deco


@intent(r'\b(hi|hello|hey|buenos dias)\b', "greet")
def handle_greet(s: Session, _: Dict[str, Any]) -> str:
    if s.user_name:
        return f'Hello {s.user_name}! How can I help you today?'
    else:
        return "Hello! What's your name?"


@intent(r"\bmy name is (?P<name>[A-Za-z \-']{2,40})\b", "set_name")
def handle_set_name(s: Session, data: Dict[str, Any]) -> str:
    name = data.get("name")
    if name is None:
        return "Sorry, I didn't catch your name. Please tell me again."
    s.user_name = name
    s.last_intent = "set_name"
    return f'Nice to meet you, {name}! How can I help you today?'


@intent(r"\b(what time is it|time|date)\b", "time")
def handle_time(s: Session, _: Dict[str, Any]) -> str:
    s.last_intent = "time"
    now = datetime.now()
    return f"It's {now.strftime('%H:%M')} on {now.strftime('%Y-%m-%d')}."


@intent(r"\b(coin|flip a coin)\b", "coin_flip")
def handle_flip(s: Session, _: Dict[str, Any]) -> str:
    import random
    s.last_intent = "coin_flip"
    return "Heads!" if random.random() > 0.5 else "Tails!"


def handle_fallback(s: Session, _: Dict[str, Any]) -> str:
    s.last_intent = "fallback"
    return "I'm not sure I understand. Try: 'my name is ...', 'what time is it' or 'what is 12*7'."


def reply(s: Session, text: str) -> str:
    s.turns += 1
    text = text.strip()
    i, h, d = router.match(text)
    if h:
        return h(s, d)

    return handle_fallback(s, {})


def main():
    session = load_memory()
    try:
        while True:
            user_input = input("> ")
            if user_input.strip().lower() == "quit":
                break
            response = reply(session, user_input)
            print(response)
    finally:
        save_memory(session)


if __name__ == "__main__":
    main()
