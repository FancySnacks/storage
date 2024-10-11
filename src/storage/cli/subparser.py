"""Subcommands for the argument parser"""

from __future__ import annotations

import argparse
from abc import ABC, abstractmethod
from argparse import ArgumentParser

from storage.const import ComponentType, get_component_types


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())

        positional_args: list[str] = []
        comparison_args: list[str] = []

        for value in values:
            try:
                operator = self.get_operator(value)
            except ValueError:
                positional_args.append(value)
                continue
            else:
                if operator == "=" and not self.range_operator_exists(value):
                    key, value = value.split(operator)
                    getattr(namespace, self.dest)[key] = value
                else:
                    key, value = value.split(operator)
                    item = f"{key}{operator}{value}"
                    comparison_args.append(item)

        setattr(namespace, 'tags_positional', positional_args)
        setattr(namespace, 'tags_comparison', comparison_args)

    def get_operator(self, value: str) -> str:
        operators = ["<", ">", "<=", ">=", "="]

        for op in operators:
            if op in value:
                return op

        raise ValueError("No operator ['=', '<', '>', '<=', '>='] has been passed!")

    def range_operator_exists(self, value: str) -> bool:
        if '-' in value:
            return True
        else:
            return False



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
        self.parser: ArgumentParser = self.parser_parent.subparsers.add_parser(self.subparser_name,
                                                                               help=self.help)
        self.children_parsers = self.parser.add_subparsers(help=self.subparsers_help)
        self.post_init()

    def get_formatted_usage_text(self) -> str:
        prog_name = self.parser_parent.parser.prog
        return f'{prog_name} {self.subparser_name} {self.get_children_parsers_names_as_formatted_str()} [options]'

    def get_children_parsers_names_as_formatted_str(self) -> str:
        names = self.children_parsers.choices
        return '{' + ', '.join(names) + '}'

    def post_init(self):
        self.parser.usage = self.get_formatted_usage_text()


class CreateSubparser(Subparser):
    subparser_name = 'create'
    help: str = 'Create new container, drawer or component at target destination.'
    subparsers_help: str = 'Choose item to create'

    def initialize_subparser(self):
        super().initialize_subparser()

        # ===== CREATE CONTAINER ===== #

        create_container_parser: ArgumentParser = self.children_parsers.add_parser('container')

        create_container_parser.add_argument('name',
                                             type=str,
                                             metavar="NAME",
                                             help="Container name")

        create_container_parser.add_argument('rows',
                                             type=int,
                                             metavar="ROWS",
                                             help="Number of rows")

        create_container_parser.add_argument('columns',
                                             type=int,
                                             metavar="COLUMNS",
                                             help="Number of maximum columns (drawers) per row")

        create_container_parser.add_argument('--separators',
                                             type=int,
                                             default=3,
                                             metavar="SEPARATORS",
                                             help="Number of compartments/separators per drawer - aka max count of "
                                                  "unique components in a single drawer")

        create_container_parser.add_argument('--tags',
                                             action=ParseKwargs,
                                             nargs='*',
                                             type=str,
                                             metavar="TAGS",
                                             default={},
                                             help="Custom tags defined by the user, used for searching commands.\n"
                                                  "Arguments should be passed as 'key=value' pairs, "
                                                  "separated by spaces.\n"
                                                  "Example: 'manufacturer=StrongBox' 'model=W201A'"
                                                  "Some tags are created automatically by passed positional args.")

        # ===== CREATE DRAWER ===== #

        create_drawer_parser: ArgumentParser = self.children_parsers.add_parser('drawer')

        create_drawer_parser.add_argument('name',
                                          type=str,
                                          metavar="NAME",
                                          help="Drawer name")

        create_drawer_parser.add_argument('container',
                                          type=str,
                                          metavar="PARENT_CONTAINER_NAME",
                                          help="Parent container name")

        create_drawer_parser.add_argument('--separators',
                                          type=int,
                                          default=3,
                                          metavar="SEPARATORS",
                                          help="Number of compartments/separators per drawer - aka max count of "
                                               "unique components in a single drawer")

        create_drawer_parser.add_argument('--row',
                                          type=int,
                                          default=-1,
                                          metavar="ROW")

        create_drawer_parser.add_argument('--column',
                                          type=int,
                                          default=-1,
                                          metavar="COLUMN")

        create_drawer_parser.add_argument('--tags',
                                          action=ParseKwargs,
                                          nargs='*',
                                          type=str,
                                          metavar="TAGS",
                                          default={},
                                          help="Custom tags defined by the user, used for searching commands.\n"
                                               "Arguments should be passed as 'key=value' pairs, "
                                               "separated by spaces.\n"
                                               "Example: 'depth=10cm' 'color=red'"
                                               "Some tags are created automatically by passed positional args.")
        # ===== CREATE COMPONENT ===== #

        create_component_parser: ArgumentParser = self.children_parsers.add_parser('component')

        create_component_parser.add_argument('name',
                                             type=str,
                                             metavar="NAME",
                                             help="Component name")

        create_component_parser.add_argument('count',
                                             type=int,
                                             metavar="COUNT",
                                             help="Number of components")

        create_component_parser.add_argument('type',
                                             type=str,
                                             metavar="TYPE",
                                             choices=get_component_types(ComponentType),
                                             help="Component type. "
                                                  f"Choices: {get_component_types(ComponentType)}")

        create_component_parser.add_argument('drawer',
                                             type=str,
                                             metavar="PARENT_DRAWER_NAME",
                                             help="Parent drawer name")

        create_component_parser.add_argument('container',
                                             type=str,
                                             metavar="PARENT_CONTAINER_NAME",
                                             help="Parent container name")

        create_component_parser.add_argument('--compartment',
                                             '--c',
                                             type=int,
                                             default=-1,
                                             metavar="COMPARTMENT")

        create_component_parser.add_argument('--tags',
                                             action=ParseKwargs,
                                             nargs='*',
                                             type=str,
                                             metavar="TAGS",
                                             default={},
                                             help="Custom tags defined by the user, used for searching commands.\n"
                                                  "Arguments should be passed as 'key=value' pairs, "
                                                  "separated by spaces.\n"
                                                  "Example: 'max_current=500mA' 'type=NPN'"
                                                  "Some tags are created automatically by passed positional args.")


class GetSubparser(Subparser):
    subparser_name: str = 'get'
    help: str = 'Print out information about target item.'
    subparsers_help: str = 'Choose item to retrieve'

    def add_shared_arguments(self):
        for parser in self.children_parsers.choices.values():
            self.add_verbosity_flag(parser)

    def add_verbosity_flag(self, parser):
        parser.add_argument('-v',
                            '--verbose',
                            action='count',
                            default=1,
                            dest='verbosity',
                            help="Verbosity level of console output")

    def initialize_subparser(self):
        super().initialize_subparser()

        # ===== GET CONTAINER ===== #

        get_container_parser: ArgumentParser = self.children_parsers.add_parser('container')

        get_container_parser.add_argument('name',
                                          type=str,
                                          metavar="NAME",
                                          help="Container name")

        # ===== GET DRAWER ===== #

        get_drawer_parser: ArgumentParser = self.children_parsers.add_parser('drawer')

        get_drawer_parser.add_argument('name',
                                       type=str,
                                       metavar="NAME",
                                       help="Drawer name")

        get_drawer_parser.add_argument('container',
                                       type=str,
                                       metavar="PARENT_CONTAINER_NAME",
                                       help="Parent container name")

        # ===== GET COMPONENT ===== #

        get_component_parser: ArgumentParser = self.children_parsers.add_parser('component')

        get_component_parser.add_argument('name',
                                          type=str,
                                          metavar="NAME",
                                          help="Component name")

        get_component_parser.add_argument('drawer',
                                          type=str,
                                          metavar="PARENT_DRAWER_NAME",
                                          help="Parent drawer name")

        get_component_parser.add_argument('container',
                                          type=str,
                                          metavar="PARENT_CONTAINER_NAME",
                                          help="Parent container name")

        self.add_shared_arguments()


class FindSubparser(Subparser):
    subparser_name: str = 'find'
    help: str = 'Search for target item or group of items.'
    subparsers_help: str = 'Choose item to find'

    def add_shared_arguments(self):
        for parser in self.children_parsers.choices.values():
            self.add_verbosity_flag(parser)
            self.add_sort_argument(parser)
            self.add_count_argument(parser)
            self.add_mode_parser(parser)

    def add_verbosity_flag(self, parser):
        parser.add_argument('-v',
                            '--verbose',
                            action='count',
                            default=1,
                            dest='verbosity',
                            help="Verbosity level of console output")

    def add_sort_argument(self, parser):
        parser.add_argument('--sort',
                            type=str,
                            default='accuracy',
                            help="Sort returned items via specific key\n"
                                 "Applied after filtering")

        parser.add_argument('--reverse',
                            action='store_true',
                            help="Return sorted items in reverse order, does nothing without '--sort' argument")

    def add_count_argument(self, parser):
        parser.add_argument('--count',
                            type=str,
                            metavar="MAX_COUNT",
                            help="Max amount of printed results, applied after filtering and sorting.")

    def add_mode_parser(self, parser):
        parser.add_argument('--mode',
                            type=str,
                            metavar="SEARCH_MODE",
                            default='any',
                            choices=['all', 'any'],
                            help="Search mode\n"
                                 "'all' - find all items that match ALL the provided tags\n"
                                 "'any' - find all items that match ANY of the provided tags\n")


    def initialize_subparser(self):
        super().initialize_subparser()

        # ===== FIND CONTAINER ===== #

        find_container_parser: ArgumentParser = self.children_parsers.add_parser('container')

        find_container_parser.add_argument('tags',
                                           action=ParseKwargs,
                                           nargs='*',
                                           type=str,
                                           metavar="TAGS",
                                           default={},
                                           help="Enter tags that searched items have to match.\n"
                                                "Arguments should be passed as strings or as 'key=value' pairs, "
                                                "separated by spaces.\n"
                                                "Example: 'manufacturer=StrongBox' 'model=AE86'"
                                                "Some tags are created automatically by passed positional args.")

        # ===== FIND DRAWER ===== #

        find_drawer_parser: ArgumentParser = self.children_parsers.add_parser('drawer')

        find_drawer_parser.add_argument('--container',
                                        type=str,
                                        metavar="CONTAINER_NAME",
                                        help="Parent container name")

        find_drawer_parser.add_argument('tags',
                                        action=ParseKwargs,
                                        nargs='*',
                                        type=str,
                                        metavar="TAGS",
                                        default={},
                                        help="Enter tags that searched items have to match.\n"
                                             "Arguments should be passed as strings or as 'key=value' pairs, "
                                             "separated by spaces.\n"
                                             "Example: 'depth=10cm' 'color=red'"
                                             "Some tags are created automatically by passed positional args.")

        # ===== FIND COMPONENT ===== #

        find_component_parser: ArgumentParser = self.children_parsers.add_parser('component')

        find_component_parser.add_argument('--container',
                                           type=str,
                                           metavar="CONTAINER_NAME",
                                           help="Parent container name")

        find_component_parser.add_argument('tags',
                                           action=ParseKwargs,
                                           nargs='*',
                                           type=str,
                                           metavar="TAGS",
                                           default={},
                                           help="Enter tags that searched items have to match.\n"
                                                "Arguments should be passed as strings or as 'key=value' pairs, "
                                                "separated by spaces.\n"
                                                "Example: 'max_current=500mA' 'type=NPN'"
                                                "Some tags are created automatically by passed positional args.")

        self.add_shared_arguments()


class DeleteSubparser(Subparser):
    subparser_name: str = 'delete'
    help: str = 'Delete target container or drawer/component from its parent.'
    subparsers_help: str = 'Choose item to delete'

    def initialize_subparser(self):
        super().initialize_subparser()

        # ===== DELETE CONTAINER ===== #

        delete_container_parser: ArgumentParser = self.children_parsers.add_parser('container')

        delete_container_parser.add_argument('name',
                                             type=str,
                                             metavar="NAME",
                                             help="Container name")

        delete_container_parser.add_argument('-f',
                                             '--forced',
                                             action='store_true',
                                             default=False,
                                             help="Delete container even if it has children drawers", )

        # ===== DELETE DRAWER ===== #

        delete_drawer_parser: ArgumentParser = self.children_parsers.add_parser('drawer')

        delete_drawer_parser.add_argument('name',
                                          type=str,
                                          metavar="NAME",
                                          help="Drawer name")

        delete_drawer_parser.add_argument('container',
                                          type=str,
                                          metavar="PARENT_CONTAINER_NAME",
                                          help="Parent container name")

        delete_drawer_parser.add_argument('-f',
                                          '--forced',
                                          action='store_true',
                                          default=False,
                                          help="Delete drawer even if it has children components", )

        # ===== DELETE COMPONENT ===== #

        delete_component_parser: ArgumentParser = self.children_parsers.add_parser('component')

        delete_component_parser.add_argument('name',
                                             type=str,
                                             metavar="NAME",
                                             help="Component name")

        delete_component_parser.add_argument('drawer',
                                             type=str,
                                             metavar="PARENT_DRAWER_NAME",
                                             help="Parent drawer name")

        delete_component_parser.add_argument('container',
                                             type=str,
                                             metavar="PARENT_CONTAINER_NAME",
                                             help="Parent container name")


class ClearSubparser(Subparser):
    subparser_name: str = 'clear'
    help: str = 'Clear target item out of children items.'
    subparsers_help: str = 'Choose item to clear'

    def initialize_subparser(self):
        super().initialize_subparser()

        # ===== CLEAR CONTAINER ===== #

        clear_container_parser: ArgumentParser = self.children_parsers.add_parser('container')

        clear_container_parser.add_argument('name',
                                            type=str,
                                            metavar="NAME",
                                            help="Container name")

        # ===== CLEAR DRAWER ===== #

        clear_drawer_parser: ArgumentParser = self.children_parsers.add_parser('drawer')

        clear_drawer_parser.add_argument('name',
                                         type=str,
                                         metavar="NAME",
                                         help="Drawer name")

        clear_drawer_parser.add_argument('container',
                                         type=str,
                                         metavar="PARENT_CONTAINER_NAME",
                                         help="Parent container name")
