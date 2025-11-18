import re
import os
import json
from datetime import datetime
from typing import Callable, Dict, Any, Optional

MEMORY_PATH = "memory.json"

REGISTRY: list[tuple[re.Pattern[str], str, Callable]] = []


def intent(pattern: str, name: str):
    def deco(fn):
        REGISTRY.append((re.compile(pattern, re.I), name, fn))
        return fn

    return deco


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

    def extend(self, routes: list[tuple[re.Pattern[str], str, Callable]]):
        for pattern, intent, handler in routes:
            self.add(pattern.pattern, intent, handler)

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


def handle_set_name(s: Session, data: Dict[str, Any]) -> str:
    name = data.get("name")
    if name:
        s.user_name = name.strip().title()
        s.last_intent = "set_name"
        return f"Nice to meet you, {s.user_name}."
    return "Sorry, I didn’t catch the name."


def handle_time(s: Session, _: Dict[str, Any]) -> str:
    s.last_intent = "time"
    now = datetime.now()
    return f"It’s {now.strftime('%H:%M')} on {now.strftime('%Y-%m-%d')}."


def handle_smalltalk(s: Session, _: Dict[str, Any]) -> str:
    s.last_intent = "smalltalk"
    return "I’m good, thanks for asking. What would you like to do next?"


def safe_math_eval(expr: str) -> Optional[float]:
    if not re.fullmatch(r"[0-9.\s+\-*/()]+", expr):
        return None
    try:
        return float(eval(expr, {"__builtins__": None}, {}))
    except Exception:
        return None


def handle_math(s: Session, data: Dict[str, Any]) -> str:
    s.last_intent = "math"
    expr = data.get("expr", "")
    val = safe_math_eval(expr)
    if val is None:
        return "I can only do basic arithmetic like 12*(3+4)/5."
    out = int(val) if val.is_integer() else val
    return f"{expr} = {out}"


def handle_fallback(s: Session, _: Dict[str, Any]) -> str:
    s.last_intent = "fallback"
    return "I’m not sure I understood. Try: 'my name is …', 'what time is it', or 'what is 12*7'."


router.add(r'\b(hi|hello|hey|buenos dias)\b', "greet", handle_greet)
router.add(r"\bmy name is (?P<name>[A-Za-z \-']{2,40})\b", "set_name", handle_set_name)
router.add(r"\b(what time is it|time|date)\b", "time", handle_time)
router.add(r"\b(how are you|what's up)\b", "smalltalk", handle_smalltalk)
router.add(r"\bwhat is (?P<expr>[0-9\.\s\+\-\*\/\(\)]+)\b", "math", handle_math)

@intent(r"\b(coin|flip a coin)\b", "coin_flip")
def coin_flip(session, _data: Dict[str, Any]) -> str:
    import random
    session.last_intent = "coin_flip"
    return "Heads" if random.random() < 0.5 else "Tails"

router.extend(REGISTRY)


def reply(s: Session, text: str) -> str:
    s.turns += 1
    text = text.strip()
    i, h, d = router.match(text)
    if h:
        return h(s, d)

    return handle_fallback(s, {})


def main():
    print("Chat v1 — type 'quit' to exit.")
    s = load_memory()
    try:
        while True:
            user = input("> ")
            if user.strip().lower() in {"quit", "exit"}:
                print("Bye.")
                break
            bot = reply(s, user)
            print(bot)
    finally:
        save_memory(s)


if __name__ == "__main__":
    main()
