from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from storage.items.drawer import Drawer
    from storage.items.position import Position


class ComponentPlaceholder:
    pass


@dataclass
class Component:
    """Singular component or a group of components stored in parent drawer."""
    name: str
    count: int
    type: str
    compartment: int
    tags: dict = field(repr=False, default_factory=dict)
    parent_drawer: Drawer = None

    @property
    def location(self) -> tuple[Position, int]:
        """Returns drawer position and compartment at which this component is located"""
        return self.parent_drawer.location, self.compartment

    def get_readable_format(self) -> str:
        return f"{self.name} (x{self.count})"

    def get_location_readable_format(self) -> str:
        return f"{self.name} at {self.location[0]} compartment {self.location[1] + 1}"

    def to_json(self) -> dict:
        return {"name": self.name,
                "count": self.count,
                "type": self.type,
                "compartment": self.compartment,
                "tags": self.tags}

    def __repr__(self) -> str:
        return self.get_readable_format()
