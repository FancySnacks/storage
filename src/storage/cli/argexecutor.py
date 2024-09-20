from abc import ABC, abstractmethod


class ArgExecutor(ABC):
    def __init__(self, argv: list[str]):
        self.argv: list[str] = argv
        self.positional_args: list[str] = self.get_positional_args_from_argv(argv)[1::]
        self.item_type: str = self.positional_args[1]
        print(self.argv)
        print(self.positional_args)

    @property
    @abstractmethod
    def name(self) -> str:
        return 'subparser'

    def get_positional_args_from_argv(self, argv: list[str]) -> list[str]:
        arg_start = argv.index(self.name) + 1
        return argv[arg_start::]

class CreateArgExecutor(ArgExecutor):
    @property
    def name(self) -> str:
        return 'create'
