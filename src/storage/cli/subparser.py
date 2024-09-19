"""Subcommands for the argument parser"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Subparser(ABC):
    subparser_name: str = 'Subparser'
    help: str = 'Help'
    subparsers_help: str = 'Choose'

    def __init__(self, parser_parent):
        self.parser_parent = parser_parent
        self.parser = None
        self.children_parsers = None

    @abstractmethod
    def initialize_subparser(self):
        self.parser = self.parser_parent.subparsers.add_parser(self.subparser_name,
                                                               help=self.help)
        self.children_parsers = self.parser.add_subparsers(help=self.subparsers_help)

    def get_formatted_usage_text(self) -> str:
        prog_name = self.parser_parent.parser.prog
        return f'{prog_name} {self.subparser_name} {self.get_children_parsers_names_as_formatted_str()} [options]'

    def get_children_parsers_names_as_formatted_str(self) -> str:
        names = self.children_parsers.choices
        return '{' + ', '.join(names) + '}'


class CreateSubparser(Subparser):
    subparser_name: str = 'create'
    help: str = 'Create new container, drawer or component at target destination.'
    subparsers_help: str = 'Choose item to create'

    def initialize_subparser(self):
        super().initialize_subparser()
        create_container_parser = self.children_parsers.add_parser('container')
        create_drawer_parser = self.children_parsers.add_parser('drawer')
        create_component_parser = self.children_parsers.add_parser('component')
        self.parser.usage = self.get_formatted_usage_text()
