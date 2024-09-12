from storage.container import Container


def main() -> int:
    c = Container(name="ECSS", total_rows=6, max_drawers_per_row=8, compartments_per_drawer=3)
    new_drawer = c.add_drawer(drawer_name='Tranzystory NPN')

    for elem in ["BC546", "BC547", "Darlington MPSA29"]:
        new_drawer.add_component(elem, "Tranzystor")

    print(new_drawer)
    print(c)

    return 0


if __name__ == '__main__':
    SystemExit(main())
