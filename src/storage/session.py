from storage.data_manager import JSONDataManager
from storage.items.container import Container
from storage.items.drawer import Drawer
from storage.items.component import Component
from storage.const import ComponentType
from storage.cli.exceptions import ContainerNotFoundError, ItemIsNotEmptyError

from storage.search import SearchQuery, SearchResult, Searcher


class Session:
    """Session is a program instance that handles data-processing tasks."""

    def __init__(self, data_manager=JSONDataManager):
        self.data_manager = data_manager()
        self.containers: list[Container] = []

    def load_container_data_from_file(self):
        self.containers = []
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

    def create_container(self, name: str, rows: int, columns: int, drawer_compartments: int = 3, tags=None,
                         **kwargs) -> Container:
        tags = {} if tags is None else tags
        tags.update({'name': name})
        new_container = Container(name, rows, columns, compartments_per_drawer=drawer_compartments, tags=tags)
        self.save_container_file_and_resync(new_container)

        return new_container

    def delete_container(self, name: str, forced=False, **kwargs):
        container_to_del = self.get_container_by_name(name)

        if (len(container_to_del.drawers) == 0) + forced > 0:
            self.data_manager.delete_container_file(name)
            self.containers.remove(container_to_del)

            print(f"'{name}' drawer was removed")
        else:
            raise ItemIsNotEmptyError(name=name, item='container', reason='because it has child drawers!')

    def clear_container(self, name: str, **kwargs):
        container_to_clear = self.get_container_by_name(name)
        container_to_clear.clear_container()

    def create_drawer(self, name: str, container: str, row: int = -1, column: int = -1, tags=None, **kwargs) -> Drawer:
        container = self.get_container_by_name(container)
        tags = {} if tags is None else tags
        tags.update({'name': name})
        new_drawer = container.add_drawer(name, int(row), int(column), tags)
        self.save_container_file_and_resync(container)

        return new_drawer

    def delete_drawer(self, name: str, container: str, forced=False, **kwargs):
        container = self.get_container_by_name(container)
        container.remove_drawer_by_name(name, forced)
        self.save_container_file_and_resync(container)

    def clear_drawer(self, name: str, container: str, **kwargs):
        container = self.get_container_by_name(container)
        drawer_to_clear = container.get_drawer_by_name(name)
        drawer_to_clear.clear_drawer()

    def create_component(self, name: str, count, type: str, container: str,
                         drawer: str, compartment: int = -1, tags=None, **kwargs) -> Component:
        container = self.get_container_by_name(container)
        drawer = container.get_drawer_by_name(drawer)

        type = ComponentType(type)
        tags = {} if tags is None else tags
        tags.update({'name': name, 'count': count, 'type': type})
        new_component = drawer.add_component(name, type, tags, int(count), compartment)
        self.save_container_file_and_resync(container)

        return new_component

    def delete_component(self, name: str, drawer: str, container: str, **kwargs):
        container = self.get_container_by_name(container)
        drawer = container.get_drawer_by_name(drawer)
        drawer.remove_component_by_name(name)
        self.save_container_file_and_resync(container)

    def get_container_by_name(self, name: str, **kwargs) -> Container:
        for container in self.containers:
            if container.name == name:
                return container

        raise ContainerNotFoundError(name=name)

    def get_drawer_by_name(self, name: str, container: str, **kwargs) -> Drawer:
        container = self.get_container_by_name(container)
        return container.get_drawer_by_name(name)

    def get_component_by_name(self, name: str, drawer: str, container: str, **kwargs) -> Component:
        container = self.get_container_by_name(container)
        drawer = container.get_drawer_by_name(drawer)
        return drawer.get_component_by_name(name)

    def print_container_info(self, name: str, verbosity: int = 1, **kwargs):
        if name == '*':
            for container in self.containers:
                print(container)

        container = self.get_container_by_name(name)
        print(container)

    def print_drawer_info(self, name: str, container: str, verbosity: int = 1, **kwargs):
        drawer = self.get_drawer_by_name(name, container)
        print(drawer)

    def print_component_info(self, name: str, drawer: str, container: str, verbosity: int = 1, **kwargs):
        component = self.get_component_by_name(name, drawer, container)
        print(component)

    def find_container(self, **kwargs):
        tags_positional: list[str] = kwargs.get('tags_positional')
        tags_keywords: dict = kwargs.get('tags')

        query = SearchQuery('all')
        searcher = Searcher(query)

        items = searcher.search_through_items(self.containers, tags_positional, tags_keywords)
        print(items)

    def find_drawer(self, **kwargs):
        tags_positional: list[str] = kwargs.get('tags_positional')
        tags_keywords: dict = kwargs.get('tags')

        query = SearchQuery('all')
        searcher = Searcher(query)

        drawers = self.containers[1].drawers
        items = searcher.search_through_items(drawers, tags_positional, tags_keywords)
        print(items)

    def find_component(self, **kwargs):
        tags_positional: list[str] = kwargs.get('tags_positional')
        tags_keywords: dict = kwargs.get('tags')

        query = SearchQuery('all')
        searcher = Searcher(query)

        comps = self.containers[1].drawers[0].components
        items = searcher.search_through_items(comps, tags_positional, tags_keywords)
        print(items)
