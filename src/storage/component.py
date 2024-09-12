from dataclasses import dataclass, field


@dataclass
class Component:
    name: str
    count: int
    type: str
    tags: dict = field(init=False, repr=False, default_factory=dict)

    def get_readable_format(self) -> str:
        return f"{self.name} (x{self.count})"

    def __repr__(self) -> str:
        return self.get_readable_format()
