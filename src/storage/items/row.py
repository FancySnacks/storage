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

    def pop_item(self, column: int = -1) -> item_class:
        old_item = self.items[column]
        self.items[column] = self.placeholder_item_class()
        return old_item

    def fill_columns(self, max_items_per_row):
        for column_n in range(0, max_items_per_row):
            self.items.append(self.placeholder_item_class())

    def get_column_length(self) -> int:
        return len([x for x in self.items if isinstance(x, self.item_class)])

    def is_column_free(self, column: int) -> bool:
        item = self.items[column]
        return isinstance(item, self.placeholder_item_class)

    def get_all_valid_items(self) -> list[item_class]:
        items = []

        for item in self.items:
            if isinstance(item, self.item_class):
                items.append(item)

        return items
