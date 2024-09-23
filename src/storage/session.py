"""Session is a program instance that handles data-processing tasks."""

from storage.data_manager import JSONDataManager
from storage.items.container import Container
from storage.items.drawer import Drawer
from storage.items.component import Component
from storage.const import ComponentType


class Session:
    def __init__(self, data_manager=JSONDataManager):
        self.data_manager = data_manager()
        self.containers: list[Container] = []

    def load_container_data_from_file(self):
        container_data = self.data_manager.load_all_container_data_from_save_directory()

        for data in container_data:
            drawers = data.pop('drawers')

            new_container = Container(**data)

            for drawer in drawers:
                print(drawer)
                new_container.add_drawer(**drawer)

            self.containers.append(new_container)

    def save_container_file_and_resync(self, container: Container):
        self.data_manager.save_data_to_file(container)
        self.load_container_data_from_file()

    def create_container(self, name: str, rows: int, columns: int, drawer_compartments: int = 3) -> Container:
        new_container = Container(name, rows, columns, compartments_per_drawer=drawer_compartments)
        self.save_container_file_and_resync(new_container)

        return new_container

    def create_drawer(self, name: str, parent_container_name: str, row_pos: int = -1, column_pos: int = -1) -> Drawer:
        container = self.get_container_by_name(parent_container_name)
        new_drawer = container.add_drawer(name, row_pos, column_pos)
        self.save_container_file_and_resync(container)
        return new_drawer

    def create_component(self, name: str, count, component_type: str) -> Component:
        component_type = ComponentType(component_type)
        new_component = Component(name, count, component_type)
        return new_component

    def get_container_by_name(self, name: str) -> Container:
        for container in self.containers:
            if container.name == name:
                return container

        raise ValueError(f"Container with name '{name}' does not exist!")
