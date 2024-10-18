from abc import ABC, abstractmethod
from typing import Callable

from storage.session import Session


class ArgExecutor(ABC):
    """Handles specific subparser by calling dedicated functions with provided args and flags."""
    name: str = 'default'

    def __init__(self, session: Session, item_type: str, parsed_args: dict):
        self.session: Session = session
        self.parsed_args = parsed_args
        self.item_type: str = item_type

    @property
    @abstractmethod
    def item_func_mapping(self) -> dict[str, Callable]:
        pass

    def parse_args(self):
        item_function_to_call = self.get_item_related_function()
        item_function_to_call(**self.parsed_args)

    def get_item_related_function(self) -> Callable:
        return self.item_func_mapping.get(self.item_type)


class CreateArgExecutor(ArgExecutor):
    """Handles 'create' subparser and executes functions related to creation of an item."""
    name: str = 'create'

    @property
    def item_func_mapping(self) -> dict[str, Callable]:
        d = {'container': self.session.create_container,
             'drawer': self.session.create_drawer,
             'component': self.session.create_component}
        return d


class GetArgExecutor(ArgExecutor):
    """Handles 'get' subparser and executes functions related to retrieving items."""
    name: str = 'get'

    @property
    def item_func_mapping(self) -> dict[str, Callable]:
        d = {'container': self.session.print_container_info,
             'drawer': self.session.print_drawer_info,
             'component': self.session.print_component_info}
        return d


class FindArgExecutor(ArgExecutor):
    """Handles 'find' subparser and executes functions related to finding items via tags."""
    name: str = 'find'

    @property
    def item_func_mapping(self) -> dict[str, Callable]:
        d = {'container': self.session.find_container,
             'drawer': self.session.find_drawer,
             'component': self.session.find_component}
        return d


class DeleteArgExecutor(ArgExecutor):
    """Handles 'delete' subparser and executes functions related to deletion of an item."""
    name: str = 'delete'

    @property
    def item_func_mapping(self) -> dict[str, Callable]:
        d = {'container': self.session.delete_container,
             'drawer': self.session.delete_drawer,
             'component': self.session.delete_component}
        return d


class ClearArgExecutor(ArgExecutor):
    """Handles 'clear' subparser and executes functions related to clearing items out of children."""
    name: str = 'clear'

    @property
    def item_func_mapping(self) -> dict[str, Callable]:
        d = {'container': self.session.clear_container,
             'drawer': self.session.clear_drawer}
        return d


class UpdateArgExecutor(ArgExecutor):
    """Handles 'update' subparser and executes functions related to updating item properties."""
    name: str = 'update'

    @property
    def item_func_mapping(self) -> dict[str, Callable]:
        d = {'container': self.session.update_container,
             'drawer': self.session.update_drawer,
             'component': self.session.update_component}
        return d
