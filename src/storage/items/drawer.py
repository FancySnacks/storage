from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from storage.const import Position
from storage.cli.exceptions import DuplicateNameError, NoFreeSpacesError, ItemNotFoundError, ItemNotFoundAtPositionError, \
    SpaceOccupiedError
from storage.items.component import Component, ComponentPlaceholder
from storage.items.row import Row

if TYPE_CHECKING:
    from storage.items.container import Container


class DrawerPlaceholder:
    pass


@dataclass
class Drawer:
    """A drawer belonging to certain container and containing specified amount of components."""
    name: str
    row: int
    column: int

    tags: dict = field(repr=False, default_factory=dict)
    parent_container: Container = None
    _row: Row = None

    def __post_init__(self):
        self.create_component_spaces()

    @property
    def location(self) -> Position:
        return Position(self.row, self.column)

    @property
    def components(self) -> list[Component]:
        return self._row.get_all_valid_items()

    @property
    def component_names(self) -> list[str]:
        return [comp.name for comp in self.components]

    @property
    def position(self) -> tuple[int, int]:
        return self.row, self.column

    def create_component_spaces(self):
        new_row = Row(0, [], Component, ComponentPlaceholder)
        self._row = new_row

        new_row.fill_columns(self.parent_container.compartments_per_drawer)

    def add_component(self, name: str, type: str, tags: dict, count: int = 0,
                      compartment: int = -1) -> Component:
        """The total limit of unique components this drawer can have is specified by drawer's container parent.\n
          Each component type belongs in its own separate compartment."""

        if self._component_already_exists(name):
            raise DuplicateNameError(item='component', name=name, relation=self.name)

        if not self._free_spot_exists(self.components):
            raise NoFreeSpacesError(item='component', relation=self.name)
        else:
            target_compartment = self._clamp_new_component_location(compartment)
            new_component = Component(name, count, type, parent_drawer=self,
                                      compartment=target_compartment, tags=tags)
            self.move_component_to(new_component, target_compartment)

            print(f"[SUCCESS] {new_component.name} component was added to "
                  f"{self.parent_container.name}/{self.name} [{self.row},{self.column}] "
                  f"at compartment {len(self.components)}")

            return new_component

    def get_component_by_name(self, component_name: str) -> Component:
        """Get child component by name. Returns none if component wasn't found."""
        try:
            index = self.component_names.index(component_name)
            return self.components[index]
        except ValueError:
            raise ItemNotFoundError(item='component', name=component_name, relation=self.name)

    def remove_component_by_name(self, component_name: str):
        component = self.get_component_by_name(component_name)
        index = component.compartment

        if not component:
            return

        self._row.pop_item(index)
        print(f"[SUCCESS] '{component_name}' component was removed from {self.parent_container.name}/{self.name}")

    def remove_component_by_index(self, component_index: int):
        try:
            if self._row.is_column_free(component_index):
                raise ValueError

            component = self._row.pop_item(component_index)
            component_name = component.name
            print(f"[SUCCESS] '{component_name}' component was removed from {self.parent_container.name}/{self.name}")

        except ValueError:
            raise ItemNotFoundAtPositionError(item='component', relation=self.name, pos=f"index {component_index}")

    def clear_drawer(self):
        self._row.items.clear()
        self._row.fill_columns(self.parent_container.compartments_per_drawer)
        print(f"[SUCCESS] {self.name} has been cleared!")

    def move_component_to(self, component: Component, compartment: int, forced: bool = False):
        max_compartments = self.parent_container.compartments_per_drawer - 1

        if compartment > max_compartments:
            raise NoFreeSpacesError(item='component', relation=self.name,
                                    reason=f"as specified compartment number is not valid")

        if self._row.is_column_free(compartment) + forced > 0:
            self._row.pop_item(compartment)
            self._row.items[compartment] = component
            component.compartment = compartment
        else:
            raise SpaceOccupiedError(itme='component', relation=self.name, pos=f"compartment {compartment}")

    def _clamp_new_component_location(self, compartment: int = -1):
        if compartment > -1:
            if self._row.is_column_free(compartment):
                return compartment
            else:
                raise SpaceOccupiedError(itme='component', relation=self.name, pos=f"compartment {compartment}")
        else:
            return self.get_next_free_compartment()

    def get_next_free_compartment(self) -> int:
        for i, space in enumerate(self._row.items):
            if self._row.is_column_free(i):
                return i
        raise NoFreeSpacesError(item='component', relation=self.name)

    def _free_spot_exists(self, components: list[Component]) -> bool:
        """Check whether all compartments are taken or not."""
        if self.parent_container:
            if len(components) < self.parent_container.compartments_per_drawer:
                return True

        return False
    
    def _component_already_exists(self, component_name) -> bool:
        if component_name in self.component_names:
            return True
        return False

    def get_readable_format(self) -> str:
        components = [f"{comp.get_readable_format()}" for comp in self.components]
        components = ', '.join(components)
        return f"[DRAWER] {self.get_pos_str()} {self.name} [{components}]\n"

    def get_pos_str(self) -> str:
        """Get drawer position in storage as formatted string."""
        return f"[{self.row},{self.column}]"

    def _row_to_dict_list(self) -> list[dict]:
        return [comp.to_json() for comp in self.components]

    def to_json(self) -> dict:
        return {"name": self.name,
                "row": self.row,
                "column": self.column,
                "tags": self.tags,
                "components": self._row_to_dict_list()}

    def __repr__(self) -> str:
        return self.get_readable_format()
