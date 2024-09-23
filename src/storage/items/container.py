from __future__ import annotations

from dataclasses import dataclass, field

from storage.items.drawer import Drawer, DrawerPlaceholder
from storage.items.component import Component


@dataclass
class Row:
    """Singular row of drawers belonging to a container."""
    index: int
    drawers: list[Drawer | DrawerPlaceholder]

    def pop_drawer(self, column: int = -1) -> Drawer:
        old_drawer = self.drawers[column]
        self.drawers[column] = DrawerPlaceholder()
        return old_drawer

    def fill_columns(self, max_drawers_per_row):
        for column_n in range(0, max_drawers_per_row):
            self.drawers.append(DrawerPlaceholder())

    def get_column_length(self) -> int:
        return len([x for x in self.drawers if isinstance(x, Drawer)])

    def is_column_free(self, column: int) -> bool:
        item = self.drawers[column]
        return isinstance(item, DrawerPlaceholder)


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

    @property
    def drawers(self) -> list[Drawer]:
        return self._drawers

    @property
    def get_max_drawer_count(self) -> int:
        return self.total_rows * self.max_drawers_per_row

    def __post_init__(self):
        self.create_rows()

    def create_rows(self, fill_empty_spaces=True):
        for row_n in range(0, self.total_rows):
            new_row = Row(row_n, [])
            self.drawer_rows.append(new_row)

            if fill_empty_spaces:
                new_row.fill_columns(self.max_drawers_per_row)

    def resize_container(self, rows: int, drawers_per_row: int):
        self.total_rows = rows
        self.max_drawers_per_row = drawers_per_row
        self.clear_container()

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

        row = self.drawer_rows[pos.row]
        row.drawers[pos.column] = new_drawer
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
            return self.drawer_rows[row].drawers[column]
        except IndexError:
            print(f"[FAIL] Drawer at {Position(row, column)} was not found inside {self.name} container.")
            return None

    def remove_drawer_by_name(self, drawer_name: str):
        drawer = self.get_drawer_by_name(drawer_name)

        if not drawer:
            return

        self.drawer_rows[drawer.row].pop_drawer(drawer.column)
        self._drawers.remove(drawer)

        print(f"[SUCCESS] '{drawer_name}' drawer was removed from {self.name}")

    def remove_drawer_at_pos(self, row: int, column: int):
        drawer = self.get_drawer_at_pos(row, column)

        if not drawer:
            return None

        drawer = self.drawer_rows[row].pop_drawer(column)
        self._drawers.remove(drawer)

        print(f"[SUCCESS] '{drawer.name}' drawer at {Position(row, column)} was removed from {self.name}")

    def move_drawer_to(self, drawer_obj: Drawer, row: int, column: int, forced=False):
        target_row = self.drawer_rows[row]
        is_space_free = target_row.is_column_free(column)
        old_pos = drawer_obj.position

        if is_space_free + forced > 0:
            target_row.drawers[column] = drawer_obj
            drawer_obj.row = row
            drawer_obj.column = column
            self.drawer_rows[old_pos[0]].drawers[old_pos[1]] = DrawerPlaceholder()
        else:
            raise ValueError("[FAIL] Failed move the drawer as that column is occupied by another!")

    def clear_container(self):
        self._drawers.clear()
        self.drawer_rows.clear()
        self.create_rows()

        print(f"[SUCCESS] {self.name} has been cleared!")

    def get_next_free_row_and_column(self) -> Position:
        """Find the first free spot where a new Drawer can be put in."""
        for row in self.drawer_rows:
            if row.get_column_length() < self.max_drawers_per_row:
                return Position(row=row.index, column=row.get_column_length())

        raise IndexError("[FAIL] Failed to add a new drawer as there is no more space in this storage!")

    def _is_drawer_name_unique(self, drawer_name: str) -> bool:
        if drawer_name in [drawer.name for drawer in self._drawers]:
            return False
        return True

    def _drawers_to_dict_list(self) -> list[dict]:
        return [drawer.to_json() for drawer in self._drawers]

    def to_json(self) -> dict:
        return {"name": self.name,
                "drawers": self._drawers_to_dict_list()}
