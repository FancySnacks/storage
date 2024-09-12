from dataclasses import dataclass, field


@dataclass
class Storage:
    name: str
    drawers: list = field(init=False, default_factory=list)
    compartments_per_drawer: int = 3
