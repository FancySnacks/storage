"""Main entry point of the software."""

from sys import argv

from storage.session import Session
from storage.cli.parser import ArgParser
from storage.cli.subparser import CreateSubparser, GetSubparser, FindSubparser, DeleteSubparser, ClearSubparser, \
    UpdateSubparser, was_subparser_specified
from storage.cli.argexecutor import ArgExecutor, CreateArgExecutor, GetArgExecutor, FindArgExecutor, DeleteArgExecutor, \
    ClearArgExecutor, UpdateArgExecutor


def get_arg_executor_from_argv(session, item_type: str, parsed_args: dict, args: list[str]) -> ArgExecutor:
    if 'create' in args:
        return CreateArgExecutor(session, item_type, parsed_args)

    if 'get' in args:
        return GetArgExecutor(session, item_type, parsed_args)

    if 'find' in args:
        return FindArgExecutor(session, item_type, parsed_args)

    if 'delete' in args:
        return DeleteArgExecutor(session, item_type, parsed_args)

    if 'clear' in args:
        return ClearArgExecutor(session, item_type, parsed_args)

    if 'update' in args:
        return UpdateArgExecutor(session, item_type, parsed_args)

    raise ValueError("Cannot initialize a valid subparser!")


def setup_subparsers(parser: ArgParser):
    parser.add_subparser(CreateSubparser(parser))
    parser.add_subparser(GetSubparser(parser))
    parser.add_subparser(FindSubparser(parser))
    parser.add_subparser(DeleteSubparser(parser))
    parser.add_subparser(ClearSubparser(parser))
    parser.add_subparser(UpdateSubparser(parser))


def main(args: list[str] | None = None) -> int:
    session = Session()
    parser = ArgParser()

    session.load_container_data_from_file()
    parser.setup_args()
    setup_subparsers(parser)

    parsed_args: dict = parser.parse_args(args)

    if parsed_args.get('printargs'):
        print(parsed_args)

    if len(argv) > 2:
        item_type = argv[2]
        arg_executor = get_arg_executor_from_argv(session, item_type, parsed_args, argv)
        arg_executor.parse_args()
    elif not was_subparser_specified(argv):
        raise ValueError(f"You attempted to use '{argv[1]}' but did not specify an item: "
                         "{container, drawer, component}")

    return 0


if __name__ == '__main__':
    SystemExit(main())
