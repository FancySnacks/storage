from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from storage.component import Component

if TYPE_CHECKING:
    from storage.container import Container


@dataclass
class Drawer:
    """A drawer belonging to certain container and containing specified amount of components."""
    name: str
    row: int
    column: int

    components: list[Component] = field(default_factory=list)
    parent_container: Container = None

    def __post_init__(self):
        self.components = []

    @property
    def component_names(self) -> list[str]:
        return [comp.name for comp in self.components]

    def add_component(self, component_name: str, component_type: str, count: int = 0) -> Component | None:
        """Add a new component to this drawer.\n
        The total limit of unique components this drawer can have is specified by drawer's container parent.\n
        Each component type belongs in its own separate compartment."""

        if self._component_already_exists(component_name):
            print(f"[FAIL] Failed to add component '{component_name}' to {self.parent_container.name}/{self.name} as it"
                  f" already exists.")
            return None

        if not self._too_many_components(self.components):
            new_component = Component(component_name, count, component_type)
            self.components.append(new_component)

            print(f"[SUCCESS] {new_component.name} component was added to "
                  f"{self.parent_container.name}/{self.name} [{self.row},{self.column}] "
                  f"at compartment {len(self.components)}")
            
            return new_component
        
        else:
            print(f"Too many component types to fit in a single drawer "
                  f"({len(self.components)}/{self.parent_container.compartments_per_drawer})")
            return None

    def get_component_by_name(self, component_name: str) -> Component | None:
        """Get child component by name. Returns none if component wasn't found."""
        try:
            index = self.component_names.index(component_name)
            return self.components[index]
        except ValueError:
            print(f"[FAIL] '{component_name}' component was not found in {self.parent_container.name}/{self.name}!")
            return None

    def remove_component_by_name(self, component_name: str):
        component = self.get_component_by_name(component_name)
        index = self.component_names.index(component_name)

        if not component:
            return

        self.components.pop(index)
        print(f"[SUCCESS] '{component_name}' component was removed from {self.parent_container.name}/{self.name}")

    def remove_component_by_index(self, component_index: int):
        try:
            component = self.components.pop(component_index)
            component_name = component.name
            print(f"[SUCCESS] '{component_name}' component was removed from {self.parent_container.name}/{self.name}")
        except ValueError:
            print(f"[FAIL] Component at index '{component_index}' was not found in "
                  f"{self.parent_container.name}/{self.name}!")

    def _too_many_components(self, components: list[Component]) -> bool:
        """Check whether all compartments are taken or not."""
        if self.parent_container:
            if len(components) > self.parent_container.compartments_per_drawer:
                return True

        return False
    
    def _component_already_exists(self, component_name) -> bool:
        if component_name in self.component_names:
            return True
        return False

    def get_readable_format(self) -> str:
        components = [f"{comp.get_readable_format()}" for comp in self.components]
        components = ', '.join(components)
        return f"{self.get_pos_str()} {self.name} [{components}]\n"

    def get_pos_str(self) -> str:
        """Get drawer position in storage as formatted string."""
        return f"[{self.row},{self.column}]"

    def __repr__(self) -> str:
        return self.get_readable_format()
