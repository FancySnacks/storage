from __future__ import annotations

from dataclasses import dataclass, field
from typing import NamedTuple, TYPE_CHECKING

from drawer import Drawer
from component import Component


class Row(NamedTuple):
    index: int
    drawers: list[Drawer]


class Position(NamedTuple):
    row: int
    column: int


@dataclass
class Container:
    name: str
    total_rows: int
    max_drawers_per_row: int = 8
    compartments_per_drawer: int = 3

    drawer_rows: list[Row] = field(default_factory=list)

    def __post_init__(self):
        for i in range(0, self.total_rows):
            new_row = Row(i, [])
            self.drawer_rows.append(new_row)

    def add_drawer(self, drawer_name: str, components: list[Component] = list) -> Drawer:
        pos = self.get_next_free_row_and_column()
        new_drawer = Drawer(drawer_name, pos.row, pos.column, components=components, parent_container=self)
        self.drawer_rows[pos.row].drawers.append(new_drawer)

        print(f"[DRAWER] {new_drawer.name} was added to "
              f"{self.name} at [{pos.row},{pos.column}]")
        
        return new_drawer

    def get_next_free_row_and_column(self) -> Position:
        for row in self.drawer_rows:
            if c := len(row.drawers) < self.max_drawers_per_row:
                return Position(row=row.index, column=c)

        raise IndexError("[FAIL] Failed to add a new drawer as there is no more space in this storage!")
