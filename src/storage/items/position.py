"""Printable class representing x,y coordinates of a drawer"""

from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from storage.items.drawer import Drawer


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
