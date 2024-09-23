from __future__ import annotations

from dataclasses import dataclass, field

from storage.items.row import Row
from storage.items.drawer import Drawer, DrawerPlaceholder


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
            new_row = Row(row_n, [], Drawer, DrawerPlaceholder)
            self.drawer_rows.append(new_row)

            if fill_empty_spaces:
                new_row.fill_columns(self.max_drawers_per_row)

    def resize_container(self, rows: int, drawers_per_row: int):
        self.total_rows = rows
        self.max_drawers_per_row = drawers_per_row
        self.clear_container()

    def add_drawer(self, name: str, row: int = -1, column: int = -1, components=None) -> Drawer:
        """Add new Drawer child class identified by unique name.\n
        List of child components can be empty.\n
        Returns a new drawer if successful."""

        if not self._is_drawer_name_unique(name):
            drawer = self.get_drawer_by_name(name)
            raise ValueError(f"Drawer with name '{name}' already exists at {Position.from_drawer(drawer)}")

        pos = self._clamp_new_drawer_position(row, column)
        new_drawer = Drawer(name, pos.row, pos.column, parent_container=self)

        if components:
            for comp in components:
                new_drawer.add_component(**comp)

        row = self.drawer_rows[pos.row]
        row.items[pos.column] = new_drawer
        self._drawers.append(new_drawer)

        print(f"{new_drawer.name} drawer was added to {self.name} at [{pos.row},{pos.column}]")
        
        return new_drawer

    def get_drawer_by_name(self, drawer_name: str) -> Drawer:
        """Return child Drawer by name. Returns None if drawer wasn't found."""
        for drawer in self._drawers:
            if drawer.name == drawer_name:
                return drawer

        raise ValueError(f"'{drawer_name}' drawer was not found inside {self.name} container.")

    def get_drawer_at_pos(self, row: int, column: int) -> Drawer:
        """Return child Drawer at target row and column."""
        try:
            return self.drawer_rows[row].items[column]
        except IndexError:
            raise ValueError(
                f"Drawer was not found inside {self.name} container at {Position(row, column)}.")

    def remove_drawer_by_name(self, drawer_name: str):
        drawer = self.get_drawer_by_name(drawer_name)

        if not drawer:
            return

        self.drawer_rows[drawer.row].pop_item(drawer.column)
        self._drawers.remove(drawer)

        print(f"'{drawer_name}' drawer was removed from {self.name}")

    def remove_drawer_at_pos(self, row: int, column: int):
        drawer = self.get_drawer_at_pos(row, column)

        if not drawer:
            return None

        drawer = self.drawer_rows[row].pop_item(column)
        self._drawers.remove(drawer)

        print(f"'{drawer.name}' drawer at {Position(row, column)} was removed from {self.name}")

    def move_drawer_to(self, drawer_obj: Drawer, row: int, column: int, forced=False):
        target_row = self.drawer_rows[row]
        is_space_free = self._is_pos_free(row, column)
        old_pos = drawer_obj.position

        if is_space_free + forced > 0:
            target_row.items[column] = drawer_obj
            drawer_obj.row = row
            drawer_obj.column = column
            self.drawer_rows[old_pos[0]].items[old_pos[1]] = DrawerPlaceholder()
        else:
            raise ValueError(f"Failed move the drawer as column {column} is occupied!")

    def clear_container(self):
        self._drawers.clear()
        self.drawer_rows.clear()
        self.create_rows()

        print(f"[SUCCESS] {self.name} has been cleared!")

    def get_next_free_row_and_column(self, start_row: int = -1) -> Position:
        """Find the first free spot where a new Drawer can be put in."""
        if start_row > -1:
            row = self.drawer_rows[start_row]
            if row.get_column_length() < self.max_drawers_per_row:
                return Position(row=start_row, column=row.get_column_length())
            else:
                raise IndexError(f"Failed to add a new drawer as there are no free columns in row {start_row}!")

        for row in self.drawer_rows:
            if row.get_column_length() < self.max_drawers_per_row:
                return Position(row=row.index, column=row.get_column_length())

        raise IndexError("Failed to add a new drawer as there is no more space in this storage!")

    def _clamp_new_drawer_position(self, row: int = -1, column: int = -1):
        if row > -1:
            if not column > -1:
                raise IndexError(f"Column was specified but not row!")

            if self._is_pos_free:
                pos = Position(row, column)
            else:
                raise IndexError(f"Column {column} at row {row} is occupied!")

        else:
            pos = self.get_next_free_row_and_column()

        return pos

    def _is_pos_free(self, row: int, column: int) -> bool:
        try:
            target_row = self.drawer_rows[row]
        except IndexError:
            raise IndexError(f"Row at index '{row}' does not exist!")

        is_space_free = target_row.is_column_free(column)
        return is_space_free

    def _is_drawer_name_unique(self, drawer_name: str) -> bool:
        if drawer_name in [drawer.name for drawer in self._drawers]:
            return False
        return True

    def _drawers_to_dict_list(self) -> list[dict]:
        return [drawer.to_json() for drawer in self._drawers]

    def to_json(self) -> dict:
        return {"name": self.name,
                "total_rows": self.total_rows,
                "max_drawers_per_row": self.max_drawers_per_row,
                "compartments_per_drawer": self.compartments_per_drawer,
                "drawers": self._drawers_to_dict_list()}
