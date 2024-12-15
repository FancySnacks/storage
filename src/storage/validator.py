"""Validator class serving as a dataclass property in validating variable changes"""

from abc import ABC, abstractmethod
from sys import argv


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
                    overflowing_drawers = self.get_overflowing_drawers(overflowing_rows)

                    if 'pytest' not in argv[0]:
                        prompter = Prompter(len(overflowing_drawers),
                                            len(self.get_not_salvageable_items(value, overflowing_drawers)),
                                            'rows')
                        user_input = prompter.get_user_input()

                        if user_input:
                            setattr(obj, self.private_name, value)
                            self.reassign(value, overflowing_rows)
                        else:
                            print("Action aborted")

                    else:
                        setattr(obj, self.private_name, value)
                        self.reassign(value, overflowing_rows)
                else:
                    setattr(obj, self.private_name, value)
        else:
            setattr(obj, self.private_name, value)

    def reassign(self, new_row_count: int, overflowing_rows: list):
        overflowing_drawers = self.get_overflowing_drawers(overflowing_rows)
        drawers_to_delete = self.get_not_salvageable_items(new_row_count, overflowing_drawers)

        # drawers that will definitely get added
        overflowing_drawers = [drawer for drawer in overflowing_drawers if drawer not in drawers_to_delete]

        for drawer in overflowing_drawers:
            self.owner.move_drawer_to_a_free_spot(drawer)

        for drawer in drawers_to_delete:
            self.owner.remove_drawer_by_name(drawer.name, forced=True)

        if len(drawers_to_delete) > 0:
            print(f"{len(drawers_to_delete)} drawers were deleted")

    def get_free_spaces(self, new_row_count: int) -> list:
        # get rows with free spaces (implying the change)
        rows_with_free_spaces = self.owner.get_all_free_rows()[:new_row_count:]

        # get all free columns from all remaining rows (implying the change)
        free_columns = [row.get_free_spaces() for row in rows_with_free_spaces]
        free_columns_joined = []
        [free_columns_joined.extend(col_list) for col_list in free_columns]

        return free_columns_joined

    def get_overflowing_drawers(self, overflowing_rows: list) -> list:
        overflowing_drawers = [row.get_all_valid_items() for row in overflowing_rows]
        overflowing_drawers_joined = []
        [overflowing_drawers_joined.extend(col_list) for col_list in overflowing_drawers]
        return overflowing_drawers_joined

    def get_not_salvageable_items(self, new_row_count: int, overflowing_items: list) -> list:
        n_of_free_spaces = len(self.get_free_spaces(new_row_count)) - len(overflowing_items)
        return overflowing_items[n_of_free_spaces::]

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
                overflowing_drawers = self._get_overflowing_cols(value)

                if len(overflowing_drawers) > 0:
                    if 'pytest' not in argv[0]:
                        prompter = Prompter(len(overflowing_drawers),
                                            len(self.get_not_salvageable_items(value, overflowing_drawers)),
                                            'rows')
                        user_input = prompter.get_user_input()

                        if user_input:
                            setattr(obj, self.private_name, value)
                            self.reassign(value, overflowing_drawers)
                        else:
                            print("Action aborted")

                    else:
                        setattr(obj, self.private_name, value)
                        self.reassign(value, overflowing_drawers)
                else:
                    setattr(obj, self.private_name, value)
        else:
            setattr(obj, self.private_name, value)

    def reassign(self, new_col_count: int, overflowing_drawers: list):
        drawers_to_delete = self.get_not_salvageable_items(new_col_count, overflowing_drawers)

        # drawers that will definitely get added
        overflowing_drawers = [drawer for drawer in overflowing_drawers if drawer not in drawers_to_delete]

        for drawer in overflowing_drawers:
            self.owner.move_drawer_to_a_free_spot(drawer)

        for drawer in drawers_to_delete:
            self.owner.remove_drawer_by_name(drawer.name, forced=True)

        if len(drawers_to_delete) > 0:
            print(f"{len(drawers_to_delete)} drawers were deleted")

    def get_free_spaces(self, new_col_count: int) -> list:
        # get rows with free spaces (implying the change)
        rows_with_free_spaces = self.owner.get_all_free_rows()

        # get all free columns from all remaining rows (implying the change)
        free_columns = [row.get_free_spaces()[:new_col_count:] for row in rows_with_free_spaces]
        free_columns_joined = []
        [free_columns_joined.extend(col_list) for col_list in free_columns]

        return free_columns_joined

    def get_not_salvageable_items(self, new_col_count: int, overflowing_items: list) -> list:
        n_of_free_spaces = len(self.get_free_spaces(new_col_count)) - len(overflowing_items)
        return overflowing_items[n_of_free_spaces::]

    def _get_overflowing_cols(self, new_col_count: int) -> list:
        """Get columns that will overflow when resizing container down"""
        rows = self.owner.drawer_rows
        all_cols = [row.items for row in rows]
        overflowing_cols: list[list] = [cols[new_col_count::] for cols in all_cols]

        # join overflowing items into a single list from list of lists
        joined_overflowing_items = self._join_col_matrix(overflowing_cols)

        # remove items that act as placeholder
        joined_filtered_overflowing_items: list = [col for col in joined_overflowing_items if
                                                   rows[0].is_valid_item(col)]

        return joined_filtered_overflowing_items

    def _join_col_matrix(self, cols: list[list]) -> list:
        joined_overflowing_cols: list = []
        [joined_overflowing_cols.extend(col) for col in cols]

        return joined_overflowing_cols


class CompartmentValidator(Validator):
    def __set__(self, obj, value):
        self.owner = obj

        if hasattr(obj, self.private_name):

            if value < getattr(obj, self.private_name):
                overflowing_components = self._get_overflowing_components(value)

                if len(overflowing_components) > 0:
                    if 'pytest' not in argv[0]:
                        prompter = Prompter(len(overflowing_components),
                                            len(self.get_not_salvageable_items(value, overflowing_components)),
                                            'components')
                        user_input = prompter.get_user_input()

                        if user_input:
                            self.reassign(value, overflowing_components)
                            setattr(obj, self.private_name, value)
                        else:
                            print("Action aborted")

                    else:
                        self.reassign(value, overflowing_components)
                        setattr(obj, self.private_name, value)
                else:
                    setattr(obj, self.private_name, value)
        else:
            setattr(obj, self.private_name, value)

    def reassign(self, new_comp_count: int, overflowing_components: list):
        components_to_delete = self.get_not_salvageable_items(new_comp_count, overflowing_components)

        # components that will definitely get added
        overflowing_components = [comp for comp in overflowing_components if comp not in components_to_delete]

        for comp in overflowing_components:
            raise ValueError("TODO: Move component to a free spot")

        for comp in components_to_delete:
            comp.parent_drawer.remove_component_by_name(comp.name)

        if len(components_to_delete) > 0:
            print(f"{len(components_to_delete)} components were deleted")

    def get_free_spaces(self, new_col_count: int) -> list:
        # get drawers with free spaces (implying the change)
        drawers_with_free_spaces = self.owner.get_all_free_drawers()
        free_rows = [drawer._row for drawer in drawers_with_free_spaces if drawer.has_free_space()]

        return free_rows

    def get_not_salvageable_items(self, new_comp_count: int, overflowing_items: list) -> list:
        n_of_free_spaces = len(self.get_free_spaces(new_comp_count)) - len(overflowing_items)
        return overflowing_items[n_of_free_spaces::]

    def _get_overflowing_components(self, new_component_count: int) -> list:
        """Get columns that will overflow when resizing container down"""
        drawers = self.owner.drawers
        all_components = [drawer.components for drawer in drawers]
        overflowing_components: list[list] = [drawer[new_component_count::] for drawer in all_components]

        # join overflowing items into a single list from list of lists
        joined_overflowing_items = self._join_comp_matrix(overflowing_components)

        return joined_overflowing_items

    def _join_comp_matrix(self, comps: list[list]) -> list:
        joined_overflowing_comps: list = []
        [joined_overflowing_comps.extend(comp) for comp in comps]

        return joined_overflowing_comps


class Prompter:
    def __init__(self, overflowing_items_count: int, items_to_be_lost_count: int = 0, item_type: str = 'items'):
        self.overflowing_items_count: int = overflowing_items_count
        self.items_to_be_lost_count: int = items_to_be_lost_count
        self.item_type: str = item_type

    def get_user_input(self) -> bool:
        choice = input(
            f"WARNING: There are {self.overflowing_items_count} overflowing {self.item_type}(s).\n"
            f"If you choose to change the number of {self.item_type}s, {self.overflowing_items_count - self.items_to_be_lost_count} {self.item_type}(s) will be moved and reassigned to "
            f"remaining free spaces and {self.items_to_be_lost_count} {self.item_type}(s) will be deleted permanently.\n"
            f"Proceed anyway? (y/n)\n")

        return self._clamp_user_input(choice)

    def _clamp_user_input(self, user_input: str) -> bool:
        user_input = user_input.lower()

        match user_input:
            case 'y':
                return True
            case 'n':
                return False
            case _:
                raise ValueError("Invalid user input")
