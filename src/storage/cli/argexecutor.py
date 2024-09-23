from abc import ABC, abstractmethod
from typing import Callable

from storage.session import Session


class ArgExecutor(ABC):
    name: str = 'default'

    def __init__(self, session: Session, argv: list[str]):
        self.session: Session = session
        self.argv: list[str] = argv
        self.positional_args: list[str] = self.get_positional_args_from_argv(argv)[1::]
        self.item_type: str = self.get_item_type(argv)
        print(self.argv)
        print(self.positional_args)

    @property
    @abstractmethod
    def item_func_mapping(self) -> dict[str, Callable]:
        pass

    @abstractmethod
    def parse_args(self):
        pass

    @abstractmethod
    def get_item_related_function(self) -> Callable:
        pass

    def get_positional_args_from_argv(self, argv: list[str]) -> list[str]:
        arg_start = argv.index(self.name) + 1
        return argv[arg_start::]

    def get_item_type(self, args: list[str]) -> str:
        positionals = self.get_positional_args_from_argv(args)
        return positionals[0]

    def _normalize_args(self, args: list[str]) -> list[str]:
        return [self._arg_type_match(arg) for arg in args]

    def _arg_type_match(self, arg: str) -> int | str:
        if arg.isdigit():
            return int(arg)
        else:
            return arg


class CreateArgExecutor(ArgExecutor):
    name: str = 'create'

    @property
    def item_func_mapping(self) -> dict[str, Callable]:
        d = {'container': self.session.create_container,
             'drawer': self.session.create_drawer,
             'component': self.session.create_component}
        return d

    def get_item_related_function(self) -> Callable:
        return self.item_func_mapping.get(self.item_type)

    def parse_args(self):
        item_function_to_call = self.get_item_related_function()
        args = self._normalize_args(self.positional_args)
        item = item_function_to_call(*args)
        print(item)
