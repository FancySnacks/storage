"""Argument parser for CLI input"""

import argparse

from storage.cli.subparser import Subparser, CreateSubparser, DeleteSubparser


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="storage",
                                              description="Desc",
                                              epilog="Made by FancySnacks | 2024 | MIT License",
                                              formatter_class=argparse.RawDescriptionHelpFormatter)

        self.subparsers = self.parser.add_subparsers(title='subcommands', help="Subcommands")
        self.subparsers_obj: list[Subparser] = []
        self.parsed_args = {}

        self.setup_subparsers()
        self.setup_args()

    def parse_args(self, args_to_parse: list[str]) -> dict:
        args = self.parser.parse_args(args_to_parse)
        return args.__dict__

    def setup_args(self):
        self.parser.add_argument('--gui',
                                 action='store_true',
                                 help="Open graphical user interface.")

        self.parser.add_argument('--printargs',
                                 action='store_true',
                                 help="Print parsed arguments to console.")

    def setup_subparsers(self):
        self.add_subparser(CreateSubparser(self))
        self.add_subparser(DeleteSubparser(self))

    def add_subparser(self, subparser):
        self.subparsers_obj.append(subparser)
        subparser.initialize_subparser()
