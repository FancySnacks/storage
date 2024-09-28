"""Main entry point of the software."""

from sys import argv

from storage.session import Session
from storage.cli.parser import ArgParser
from storage.cli.subparser import CreateSubparser, DeleteSubparser, ClearSubparser, GetSubparser
from storage.cli.argexecutor import ArgExecutor, CreateArgExecutor, DeleteArgExecutor, ClearArgExecutor


def get_arg_executor_from_argv(session, args: list[str]) -> ArgExecutor:
    if 'create' in args:
        return CreateArgExecutor(session, args)

    if 'delete' in args:
        return DeleteArgExecutor(session, args)

    if 'clear' in args:
        return ClearArgExecutor(session, args)

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

    parsed_args: dict = parser.parse_args(args)
    arg_executor = get_arg_executor_from_argv(session, argv)

    if parsed_args.get('printargs'):
        print(parsed_args)

    if arg_executor:
        arg_executor.parse_args()

    return 0


if __name__ == '__main__':
    SystemExit(main())
