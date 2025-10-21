from dataclasses import dataclass

@dataclass
class Gift:
    id: int
    title: str
    person: str
    occasion: str
    priority: int
    purchased: bool
