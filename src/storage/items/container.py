from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass, field

from storage.cli.exceptions import DuplicateNameError, SpaceOccupiedError, NoFreeSpacesError, ItemNotFoundError, \
    ItemNotFoundAtPositionError, ItemIsNotEmptyError
from storage.items.row import Row
from storage.items.position import Position
from storage.items.drawer import Drawer, DrawerPlaceholder


@dataclass
class Container:
    """A container containing rows of drawers that contain groups of components allocated in many compartment
    or divisions."""
    name: str
    total_rows: int
    max_drawers_per_row: int = 8
    compartments_per_drawer: int = 3
    tags: dict = field(repr=False, default_factory=dict)

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
        self._add_special_tags()

    def _add_special_tags(self):
        self.tags['rows'] = self.total_rows
        self.tags['columns'] = self.max_drawers_per_row
        self.tags['last_update'] = datetime.now().strftime("%d/%m/%Y, %H:%M")
        self.tags['children_count'] = len(self.drawers)
        self.tags['free_space'] = all([row.has_free_space() for row in self.drawer_rows])

    def create_rows(self, fill_empty_spaces=True):
        for row_n in range(0, self.total_rows):
            new_row = Row(row_n, [], Drawer, DrawerPlaceholder)
            self.drawer_rows.append(new_row)

            if fill_empty_spaces:
                new_row.fill_columns(self.max_drawers_per_row)

    def resize_container(self, rows: int, drawers_per_row: int):
        """Change amount of rows and columns. This will remove all drawers."""
        self.total_rows = rows
        self.max_drawers_per_row = drawers_per_row
        self.clear_container()

    def add_drawer(self, name: str, row: int = -1, column: int = -1, tags=None, components=None) -> Drawer:
        """Add new Drawer child class identified by unique name.\n
        List of child components can be empty.\n
        Returns a new drawer if successful."""

        if not self._is_drawer_name_unique(name):
            drawer = self.get_drawer_by_name(name)
            raise DuplicateNameError(item='drawer', name=name, relation=self.name, pos=Position.from_drawer(drawer))

        pos = self._clamp_new_drawer_position(row, column)
        new_drawer = Drawer(name, pos.row, pos.column, parent_container=self, tags=tags or {})

        if components:
            for comp in components:
                new_drawer.add_component(**comp)

        row = self.drawer_rows[pos.row]
        row.items[pos.column] = new_drawer
        self._drawers.append(new_drawer)

        self._add_special_tags()
        print(f"{new_drawer.name} drawer was added to {self.name} at [{pos.row},{pos.column}]")

        return new_drawer

    def get_drawer_by_name(self, drawer_name: str) -> Drawer:
        """Return child Drawer by name. Returns None if drawer wasn't found."""
        for drawer in self._drawers:
            if drawer.name == drawer_name:
                return drawer

        raise ItemNotFoundError(item='drawer', name=drawer_name, relation=self.name)

    def get_drawer_at_pos(self, row: int, column: int) -> Drawer:
        """Return child Drawer at target row and column."""
        try:
            return self.drawer_rows[row].items[column]
        except IndexError:
            raise ItemNotFoundAtPositionError(item='drawer', relation=self.name, pos=Position(row, column))

    def get_all_components(self):
        """Get components of all children drawers"""
        all_comps = [drawer.components for drawer in self.drawers]
        comps_joined = []
        [comps_joined.extend(comp_list) for comp_list in all_comps]
        return comps_joined

    def remove_drawer_by_name(self, name: str, forced=False):
        drawer_to_del = self.get_drawer_by_name(name)

        if (len(drawer_to_del.components) == 0) + forced > 0:
            self.drawer_rows[drawer_to_del.row].pop_item(drawer_to_del.column)
            self._drawers.remove(drawer_to_del)

            self._add_special_tags()
            print(f"'{name}' drawer was removed from {self.name}")

        else:
            raise ItemIsNotEmptyError(name=name, item='drawer', reason='because it has child components!')

    def remove_drawer_at_pos(self, row: int, column: int):
        drawer = self.get_drawer_at_pos(row, column)

        if not drawer:
            return None

        drawer = self.drawer_rows[row].pop_item(column)
        self._drawers.remove(drawer)

        self._add_special_tags()
        print(f"'{drawer.name}' drawer at {Position(row, column)} was removed from {self.name}")

    def move_drawer_to(self, drawer_obj: Drawer, row: int, column: int, forced=False):
        """This method will fail if target location is occupied.
        Forced=True will remove drawer at target location without throwing error if it exists and
        move the desired drawer there."""
        target_row = self.drawer_rows[row]
        is_space_free = self._is_pos_free(row, column)
        old_pos = drawer_obj.position

        if is_space_free + forced > 0:
            target_row.items[column] = drawer_obj
            drawer_obj.row = row
            drawer_obj.column = column
            self.drawer_rows[old_pos[0]].items[old_pos[1]] = DrawerPlaceholder()

            self._add_special_tags()
        else:
            raise SpaceOccupiedError(itme='drawer', relation=self.name, pos=Position(row, column))

    def clear_container(self):
        self._drawers.clear()
        self.drawer_rows.clear()
        self.create_rows()
        self._add_special_tags()

        print(f"[SUCCESS] {self.name} has been cleared!")

    def get_next_free_row_and_column(self, start_row: int = -1) -> Position:
        """Find the first free spot where a new Drawer can be put in."""
        if start_row > -1:
            row = self.drawer_rows[start_row]
            if row.get_column_length() < self.max_drawers_per_row:
                return Position(row=start_row, column=row.get_column_length())
            else:
                raise NoFreeSpacesError(item='drawer', relation=self.name,
                                        reason=f"as the row {start_row} has no free spaces")

        for row in self.drawer_rows:
            if row.get_column_length() < self.max_drawers_per_row:
                return Position(row=row.index, column=row.get_column_length())

        raise NoFreeSpacesError(item='drawer', relation=self.name)

    def _clamp_new_drawer_position(self, row: int = -1, column: int = -1):
        """Place the drawer at either specified location via args or at the next free space if defaults are passed"""
        if row > -1:
            if not column > -1:
                raise ValueError(f"Column was specified but not row!")

            if self._is_pos_free(row, column):
                pos = Position(row, column)
            else:
                raise SpaceOccupiedError(item='drawer', relation=self.name, pos=Position(row, column))

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
                "tags": self.tags,
                "drawers": self._drawers_to_dict_list()}

    def __repr__(self) -> str:
        return f"[CONTAINER] {self.name} - {len(self.drawers)} drawers | {len(self.get_all_components())} components"
