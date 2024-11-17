"""Validator class serving as a dataclass property in validating changes"""

from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    @abstractmethod
    def __set__(self, obj, value):
        pass

    def __get__(self, obj, *args):
        return getattr(obj, self.private_name)


class RowValidator(Validator):
    def __set__(self, obj, value):
        self.owner = obj

        if hasattr(obj, self.private_name):

            if value < getattr(obj, self.private_name):
                overflowing_rows = self._get_overflowing_rows(value)

                if len(overflowing_rows) > 0:
                    prompter = Prompter(len(overflowing_rows), 'columns')
                else:
                    setattr(obj, self.private_name, value)

        setattr(obj, self.private_name, value)

    def _get_overflowing_rows(self, new_row_count: int) -> list:
        """Get rows that will overflow when resizing container down"""
        overflowing_rows = self.owner.drawer_rows[new_row_count::]
        overflowing_rows = [row for row in overflowing_rows if row.has_items()]
        return overflowing_rows


class ColumnValidator(Validator):
    def __set__(self, obj, value):
        self.owner = obj

        if hasattr(obj, self.private_name):

            if value < getattr(obj, self.private_name):
                overflowing_cols = self._get_overflowing_cols(value)

                if len(overflowing_cols) > 0:
                    prompter = Prompter(len(overflowing_cols), 'columns')
                else:
                    setattr(obj, self.private_name, value)

        setattr(obj, self.private_name, value)

    def _get_overflowing_cols(self, new_col_count: int) -> list:
        """Get columns that will overflow when resizing container down"""
        rows = self.owner.drawer_rows
        all_cols = [row.items for row in rows]
        overflowing_cols: list[list] = [cols[new_col_count::] for cols in all_cols]

        # join overflowing items into a single list from list of lists
        joined_overflowing_items = self._join_col_matrix(overflowing_cols)

        # remove items that act as placeholder
        joined_filtered_overflowing_items: list = [col for col in joined_overflowing_items if rows[0].is_valid_item(col)]

        return joined_filtered_overflowing_items

    def _join_col_matrix(self, cols: list[list]) -> list:
        joined_overflowing_cols: list = []
        [joined_overflowing_cols.extend(col) for col in cols]

        return joined_overflowing_cols


class Prompter:
    def __init__(self, overflowing_items_count: int, item_type: str = 'items'):
        self.choice = input(
            f"WARNING: There are {overflowing_items_count} overflowing {item_type}.\n"
            f"If you choose to change the number of columns x {item_type} will be moved and reassigned to"
            f"remaining free spaces and x {item_type} will be deleted permanently.\n"
            f"Proceed anyway? (y/n)\n")

        print(self._clamp_user_input(self.choice))

    def _clamp_user_input(self, user_input: str) -> bool:
        user_input = user_input.lower()

        match user_input:
            case 'y': return True
            case 'n': return False
            case _: raise ValueError("Invalid user input")
