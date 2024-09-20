from abc import ABC, abstractmethod

from storage.container import Container
from storage.drawer import Drawer
from storage.component import Component


class ArgExecutor(ABC):
    def __init__(self, argv: list[str]):
        self.argv: list[str] = argv
        self.positional_args: list[str] = self.get_positional_args_from_argv(argv)[1::]
        self.item_type: str = self.get_item_type(argv)
        print(self.argv)
        print(self.positional_args)

    @property
    @abstractmethod
    def name(self) -> str:
        return 'subparser'

    @abstractmethod
    def parse_args(self):
        pass

    def get_positional_args_from_argv(self, argv: list[str]) -> list[str]:
        arg_start = argv.index(self.name) + 1
        return argv[arg_start::]

    def get_item_type(self, args: list[str]) -> str:
        positionals = self.get_positional_args_from_argv(args)
        return positionals[0]

    def _normalize_args(self, args: list[str]) -> list[str]:
        return [self._arg_type_match(arg) for arg in args]

    def _arg_type_match(self, arg: str) -> int|str:
        if arg.isdigit():
            return int(arg)
        else:
            return arg

class CreateArgExecutor(ArgExecutor):
    @property
    def name(self) -> str:
        return 'create'

    def parse_args(self):
        item_mapping = {'container': Container,
                        'drawer': Drawer,
                        'component': Component}

        item_class: Container | Drawer | Component = item_mapping[self.item_type]
        item_instance = item_class(*self._normalize_args(self.positional_args))

        print(item_instance)

        raise NotImplementedError("Use actual functions like 'Container.create_drawer() or Drawer.create_component()'")
