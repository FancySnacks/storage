"""Main entry point of the software."""
import sys
from sys import argv

from storage.session import Session
from storage.cli.parser import ArgParser
from storage.cli.subparser import CreateSubparser, DeleteSubparser, ClearSubparser, GetSubparser
from storage.cli.argexecutor import ArgExecutor, CreateArgExecutor, DeleteArgExecutor, ClearArgExecutor, GetArgExecutor


def get_arg_executor_from_argv(session, item_type: str, parsed_args: dict) -> ArgExecutor:
    if 'create' in parsed_args:
        return CreateArgExecutor(session, item_type, parsed_args)

    if 'delete' in parsed_args:
        return DeleteArgExecutor(session, item_type, parsed_args)

    if 'get' in parsed_args:
        return GetArgExecutor(session, item_type, parsed_args)

    if 'clear' in parsed_args:
        return ClearArgExecutor(session, item_type,  parsed_args)

    return None


def setup_subparsers(parser: ArgParser):
    parser.add_subparser(CreateSubparser(parser))
    parser.add_subparser(GetSubparser(parser))
    parser.add_subparser(DeleteSubparser(parser))
    parser.add_subparser(ClearSubparser(parser))


def main(args: list[str] | None = None) -> int:
    session = Session()
    parser = ArgParser()

    session.load_container_data_from_file()
    parser.setup_args()
    setup_subparsers(parser)

    item_type = sys.argv[2]
    parsed_args: dict = parser.parse_args(args)

    arg_executor = get_arg_executor_from_argv(session, item_type, parsed_args)

    if parsed_args.get('printargs'):
        print(parsed_args)

    if arg_executor:
        arg_executor.parse_args()

    return 0


if __name__ == '__main__':
    SystemExit(main())
