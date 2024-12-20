from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Row:
    """Singular row of items."""
    index: int
    items: list
    item_class: Any
    placeholder_item_class: Any
    _max_items: int = 1

    def pop_item(self, column: int = -1) -> item_class:
        old_item = self.items[column]
        self.items[column] = self.placeholder_item_class()
        return old_item

    def resize(self, column_count: int):
        """Change number of columns. This action is destructive and will delete overflowing items."""
        if column_count < 1:
            raise ValueError("Column size cannot be resized below 1!")

        self._max_items = column_count
        self.items = self.items[:column_count:]

    def fill_columns(self, max_items_per_row):
        self._max_items = max_items_per_row

        for column_n in range(0, max_items_per_row):
            self.items.append(self.placeholder_item_class())

    def get_column_length(self) -> int:
        return len([x for x in self.items if isinstance(x, self.item_class)])

    def is_column_free(self, column: int) -> bool:
        item = self.items[column]
        return isinstance(item, self.placeholder_item_class)

    def has_free_space(self) -> bool:
        if self._max_items > len(self.get_all_valid_items()):
            return True
        else:
            return False

    def get_free_spaces(self) -> list[int]:
        free_cols: list[int] = []

        for index, item in enumerate(self.items):
            if not isinstance(item, self.item_class):
                free_cols.append(index)

        return free_cols

    def has_items(self) -> bool:
        return len(self.get_all_valid_items()) > 0

    def get_all_valid_items(self) -> list[item_class]:
        items = []

        for item in self.items:
            if isinstance(item, self.item_class):
                items.append(item)

        return items

    def is_valid_item(self, item) -> bool:
        return not isinstance(item, self.placeholder_item_class)
