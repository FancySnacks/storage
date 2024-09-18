"""Argument parser for CLI input"""

import argparse


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="storage",
                                              usage='%(prog)s [options]',
                                              description="Desc",
                                              epilog="Made by FancySnacks | 2024 | MIT License",
                                              formatter_class=argparse.RawDescriptionHelpFormatter)
        self.parser.add_subparsers(help="Subcommands")

        self.parsed_args = {}

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
