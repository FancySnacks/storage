from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from storage.component import Component

if TYPE_CHECKING:
    from storage.container import Container


@dataclass
class Drawer:
    name: str
    row: int
    column: int

    components: list[Component] = field(default_factory=list)
    parent_container: Container = None

    def __post_init__(self):
        self.components = []

    def add_component(self, component_name: str, component_type: str, count: int = 0) -> Component:
        if not self.too_many_components(self.components):
            new_component = Component(component_name, count, component_type)
            self.components.append(new_component)

            print(f"[COMPONENT] {new_component.name} was added to "
                  f"{self.parent_container.name}/{self.name} "
                  f"at [{self.row},{self.column}]")
            
            return new_component
        
        else:
            raise ValueError(f"Too many component types to fit in a single drawer "
                             f"({len(self.components)}/{self.parent_container.compartments_per_drawer})")

    def too_many_components(self, components: list[Component]) -> bool:
        """Make sure only as many element types are allowed as many compartments are per drawer."""
        if self.parent_container:
            if len(components) > self.parent_container.compartments_per_drawer:
                return True

        return False

    def get_readable_format(self) -> st:
        components = [f"{comp.get_readable_format()}" for comp in self.components]
        components = ', '.join(components)
        return f"{self.get_pos_str()} {self.name}\n[{components}]\n"

    def get_pos_str(self) -> str:
        """Get drawer position in storage as formatted string."""
        return f"[{self.row},{self.column}]"

    def __repr__(self) -> str:
        return self.get_readable_format()
