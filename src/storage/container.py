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
    """A class containing x,y coordinates of a drawer."""
    row: int
    column: int

    @classmethod
    def from_drawer(cls, drawer: Drawer) -> Position:
        return Position(drawer.row, drawer.column)

    def __repr__(self) -> str:
        return f"[{self.row},{self.column}]"


@dataclass(frozen=True, order=True)
class Container:
    """A container containing rows of drawers that contain groups of components allocated in many compartment
    or divisions."""
    name: str
    total_rows: int
    max_drawers_per_row: int = 8
    compartments_per_drawer: int = 3

    _drawer_rows: list[Row] = field(default_factory=list)
    _drawers: list[Drawer] = field(default_factory=list)

    @property
    def drawer_rows(self) -> list[Row]:
        return self._drawer_rows

    @property
    def drawers(self) -> list[Drawer]:
        return self._drawers

    def __post_init__(self):
        self.create_rows()

    def create_rows(self):
        self._drawer_rows.clear()

        for i in range(0, self.total_rows):
            new_row = Row(i, [])
            self._drawer_rows.append(new_row)

    def add_drawer(self, drawer_name: str, components: list[Component] = list) -> Drawer | None:
        """Add new Drawer child class identified by unique name.\n
        List of child components can be empty.\n
        Returns a new drawer if successful."""

        if not self._is_drawer_name_unique(drawer_name):
            drawer = self.get_drawer_by_name(drawer_name)
            print(f"[FAIL] Drawer with name '{drawer_name}' already exists at "
                  f"{Position.from_drawer(drawer)}")
            return None

        pos = self.get_next_free_row_and_column()
        new_drawer = Drawer(drawer_name, pos.row, pos.column, components=components, parent_container=self)

        self._drawer_rows[pos.row].drawers.append(new_drawer)
        self._drawers.append(new_drawer)

        print(f"[SUCCESS] {new_drawer.name} drawer was added to "
              f"{self.name} at [{pos.row},{pos.column}]")
        
        return new_drawer

    def get_drawer_by_name(self, drawer_name: str) -> Drawer | None:
        """Return child Drawer by name. Returns None if drawer wasn't found."""
        for drawer in self._drawers:
            if drawer.name == drawer_name:
                return drawer

        print(f"[FAIL] '{drawer_name}' drawer was not found inside {self.name} container.")
        return None

    def get_drawer_at_pos(self, row: int, column: int) -> Drawer | None:
        """Return child Drawer at target row and column."""
        try:
            return self._drawer_rows[row].drawers[column]
        except IndexError:
            print(f"[FAIL] Drawer at {Position(row, column)} was not found inside {self.name} container.")
            return None

    def remove_drawer_by_name(self, drawer_name: str):
        drawer = self.get_drawer_by_name(drawer_name)

        if not drawer:
            return

        self._drawer_rows[drawer.row].drawers.pop(drawer.column)
        self._drawers.remove(drawer)

        print(f"[SUCCESS] '{drawer_name}' drawer was removed from {self.name}")

    def remove_drawer_at_pos(self, row: int, column: int):
        drawer = self.get_drawer_at_pos(row, column)

        if not drawer:
            return None

        drawer = self._drawer_rows[row].drawers.pop(column)
        self._drawers.remove(drawer)

        print(f"[SUCCESS] '{drawer.name}' drawer at {Position(row, column)} was removed from {self.name}")

    def clear_container(self):
        self._drawers.clear()
        self.create_rows()

        print(f"[SUCCESS] {self.name} has been cleared!")

    def get_next_free_row_and_column(self) -> Position:
        """Find the first free spot where a new Drawer can be put in."""
        for row in self._drawer_rows:
            if len(row.drawers) < self.max_drawers_per_row:
                return Position(row=row.index, column=len(row.drawers))

        raise IndexError("[FAIL] Failed to add a new drawer as there is no more space in this storage!")

    def _is_drawer_name_unique(self, drawer_name: str) -> bool:
        if drawer_name in [drawer.name for drawer in self._drawers]:
            return False
        return True
