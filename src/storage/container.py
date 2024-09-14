from __future__ import annotations

from dataclasses import dataclass, field

from storage.drawer import Drawer
from storage.component import Component


@dataclass
class Row:
    """Singular row of drawers belonging to a container."""
    index: int
    drawers: list[Drawer]


@dataclass
class Position:
    """A class containing x,y coordinates of ad rawer."""
    row: int
    column: int

    def __repr__(self) -> str:
        return f"[{self.row},{self.column}]"


@dataclass
class Container:
    """A container containing rows of drawers that contain groups of components allocated in many compartment
    or divisions."""
    name: str
    total_rows: int
    max_drawers_per_row: int = 8
    compartments_per_drawer: int = 3

    drawer_rows: list[Row] = field(default_factory=list)
    _drawers: list[Drawer] = field(default_factory=list)

    def __post_init__(self):
        # Fill container with empty rows on init
        for i in range(0, self.total_rows):
            new_row = Row(i, [])
            self.drawer_rows.append(new_row)

    def add_drawer(self, drawer_name: str, components: list[Component] = list) -> Drawer:
        """Add new Drawer child class identified by unique name.\n
        List of child components can be empty.\n
        Returns a new drawer if successful, raises error if not."""
        pos = self.get_next_free_row_and_column()
        new_drawer = Drawer(drawer_name, pos.row, pos.column, components=components, parent_container=self)

        self.drawer_rows[pos.row].drawers.append(new_drawer)
        self._drawers.append(new_drawer)

        print(f"[DRAWER] {new_drawer.name} was added to "
              f"{self.name} at [{pos.row},{pos.column}]")
        
        return new_drawer

    def get_drawer_by_name(self, drawer_name: str) -> Drawer | None:
        """Return child Drawer by name."""
        for drawer in self._drawers:
            if drawer.name == drawer_name:
                return drawer

        print(f"[FAIL] '{drawer_name}' drawer was not found inside {self.name} container.")
        return None

    def get_drawer_at_pos(self, row: int, column: int) -> Drawer | None:
        """Return child Drawer at target row and column."""
        try:
            return self.drawer_rows[row].drawers[column]
        except IndexError:
            print(f"[FAIL] Drawer at {Position(row, column)} was not found inside {self.name} container.")
            return None

    def get_next_free_row_and_column(self) -> Position:
        """Find the first free spot where a new Drawer can be put in."""
        for row in self.drawer_rows:
            if len(row.drawers) < self.max_drawers_per_row:
                return Position(row=row.index, column=len(row.drawers))

        raise IndexError("[FAIL] Failed to add a new drawer as there is no more space in this storage!")
