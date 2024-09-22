"""Session is a program instance that handles data-processing tasks."""

from storage.data_manager import DataManager
from storage.items.container import Container
from storage.items.drawer import Drawer
from storage.items.component import Component
from storage.const import ComponentType


class Session:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.containers: list[Container] = []

    def load_item_data_from_file(self):
        raise NotImplementedError

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
