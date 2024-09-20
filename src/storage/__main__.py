"""Main entry point of the software."""

from storage.container import Container
from storage.cli.parser import ArgParser
from storage.cli.subparser import CreateSubparser, DeleteSubparser


def setup_subparsers(parser: ArgParser):
    parser.add_subparser(CreateSubparser(parser))
    parser.add_subparser(DeleteSubparser(parser))


def main(args: list[str] | None = None) -> int:
    parser = ArgParser()
    parser.setup_args()
    setup_subparsers(parser)

    parsed_args: dict = parser.parse_args(args)

    if parsed_args.get('printargs'):
        print(parsed_args)

    c = Container(name="ECSS", total_rows=6, max_drawers_per_row=8, compartments_per_drawer=3)
    new_drawer = c.add_drawer(drawer_name='Tranzystory NPN')

    for elem in ["BC546", "BC547", "Darlington MPSA29"]:
        new_drawer.add_component(elem, "Tranzystor")

    print(c.get_drawer_at_pos(0, 0))
    c.remove_drawer_at_pos(0, 0)

    return 0


if __name__ == '__main__':
    SystemExit(main())
