from dataclasses import dataclass, field


@dataclass
class Component:
    name: str
    count: int
    type: str
    tags: dict = field(init=False, repr=False, default_factory=dict)
