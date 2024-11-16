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
                    print("Row Overflow!")
                    # update Row list
                else:
                    setattr(obj, self.private_name, value)


        setattr(obj, self.private_name, value)

    def _get_overflowing_rows(self, new_row_count: int):
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
                    print("Column Overflow!")
                    # update Column list
                else:
                    setattr(obj, self.private_name, value)


        setattr(obj, self.private_name, value)

    def _get_overflowing_cols(self, new_col_count: int):
        """Get columns that will overflow when resizing container down"""
        return []