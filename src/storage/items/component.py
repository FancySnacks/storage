from dataclasses import dataclass, field


@dataclass
class Component:
    """Singular component or a group of components stored in parent drawer."""
    name: str
    count: int
    type: str
    tags: dict = field(init=False, repr=False, default_factory=dict)

    def get_readable_format(self) -> str:
        return f"{self.name} (x{self.count})"

    def to_json(self) -> dict:
        return {"name": self.name,
                "count": self.count,
                "type": self.type,
                "tags": self.tags}

    def __repr__(self) -> str:
        return self.get_readable_format()
