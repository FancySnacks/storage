"""Main entry point of the software."""

from storage.container import Container
from storage.cli.parser import ArgParser


def main(args: list[str] | None = None) -> int:
    parser = ArgParser()
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
