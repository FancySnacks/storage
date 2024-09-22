"""Session is a program instance that handles data-processing tasks."""

from storage.container import Container
from storage.drawer import Drawer
from storage.component import Component
from storage.const import ComponentType


class Session:
    def create_container(self, name: str, rows: int, columns: int, drawer_compartments: int = 3) -> Container:
        new_container = Container(name, rows, columns, compartments_per_drawer=drawer_compartments)
        return new_container

    def create_drawer(self, name: str, row_pos: int, column_pos: int) -> Drawer:
        new_drawer = Drawer(name, row_pos, column_pos)
        return new_drawer

    def create_component(self, name: str, count, component_type: str) -> Component:
        component_type = ComponentType(component_type)
        new_component = Component(name, count, component_type)
        return new_component
