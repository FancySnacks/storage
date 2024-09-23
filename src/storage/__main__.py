"""Main entry point of the software."""

from sys import argv

from storage.session import Session
from storage.cli.parser import ArgParser
from storage.cli.subparser import CreateSubparser, DeleteSubparser
from storage.cli.argexecutor import ArgExecutor, CreateArgExecutor


def get_arg_executor_from_argv(session, args: list[str]) -> ArgExecutor:
    if 'create' in args:
        return CreateArgExecutor(session, args)

    return ArgExecutor(session, args)


def setup_subparsers(parser: ArgParser):
    parser.add_subparser(CreateSubparser(parser))
    parser.add_subparser(DeleteSubparser(parser))


def main(args: list[str] | None = None) -> int:
    session = Session()
    parser = ArgParser()

    parser.setup_args()
    setup_subparsers(parser)
    session.load_container_data_from_file()

    parsed_args: dict = parser.parse_args(args)
    arg_executor = get_arg_executor_from_argv(session, argv)

    arg_executor.parse_args()

    if parsed_args.get('printargs'):
        print(parsed_args)

    return 0


if __name__ == '__main__':
    SystemExit(main())
