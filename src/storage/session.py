from storage.data_manager import JSONDataManager
from storage.items.container import Container
from storage.items.drawer import Drawer
from storage.items.component import Component
from storage.const import ComponentType
from storage.cli.exceptions import ContainerNotFoundError, ItemNotFoundError


class Session:
    """Session is a program instance that handles data-processing tasks."""
    def __init__(self, data_manager=JSONDataManager):
        self.data_manager = data_manager()
        self.containers: list[Container] = []

    def load_container_data_from_file(self):
        container_data = self.data_manager.load_all_container_data_from_save_directory()

        for data in container_data:
            drawers = data.pop('drawers')

            new_container = Container(**data)

            for drawer in drawers:
                new_container.add_drawer(**drawer)

            self.containers.append(new_container)

    def save_container_file_and_resync(self, container: Container):
        self.data_manager.save_data_to_file(container)
        self.load_container_data_from_file()

    def create_container(self, name: str, rows: int, columns: int, drawer_compartments: int = 3) -> Container:
        new_container = Container(name, rows, columns, compartments_per_drawer=drawer_compartments)
        self.save_container_file_and_resync(new_container)

        return new_container

    def create_drawer(self, name: str, parent_container_name: str, row: int = -1, column: int = -1) -> Drawer:
        container = self.get_container_by_name(parent_container_name)
        new_drawer = container.add_drawer(name, int(row), int(column))
        self.save_container_file_and_resync(container)

        return new_drawer

    def create_component(self, name: str, count, type: str, parent_container_name: str,
                         parent_drawer_name: str, compartment: int = -1, tags=None) -> Component:
        container = self.get_container_by_name(parent_container_name)
        drawer = container.get_drawer_by_name(parent_drawer_name)

        type = ComponentType(type)
        tags = {} if tags is None else tags
        new_component = drawer.add_component(name, type, tags, int(count), compartment)
        self.save_container_file_and_resync(container)

        return new_component

    def get_container_by_name(self, name: str) -> Container:
        for container in self.containers:
            if container.name == name:
                return container

        raise ContainerNotFoundError(name=name)

    def get_drawer_by_name(self, name: str, container_name: str) -> Drawer:
        for container in self.containers:
            if container.name == container_name:
                return container.get_drawer_by_name(name)

        raise ItemNotFoundError(name=name, type='drawer', relation=container_name)
