"""Sorts list of SearchResults instances in specific order via given key"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal

from storage.const import ITEM
from storage.search import SearchResult


def get_sorter(sorter_type: Literal['accuracy'] | str) -> Sorter:
    match sorter_type:
        case 'accuracy':
            return TagMatchCountSorter()
        case _:
            return TagValueSorter(sorter_type)


def sort_items(items: list[ITEM], sorter_name: str, reverse=False) -> list[ITEM]:
    sorter = get_sorter(sorter_name)
    items.sort(key=sorter, reverse=reverse)
    return items


class Sorter(ABC):
    @abstractmethod
    def __call__(self, search_result: SearchResult):
        return search_result.len_of_matches()


class TagMatchCountSorter(Sorter):
    """Use instance of this class as 'sort_key' when sorting items via built-in sort() function.
    Sorts items as ascending based on how many tags have been matched."""

    def __call__(self, search_result: SearchResult):
        return search_result.len_of_matches()


class TagValueSorter(Sorter):
    """Use instance of this class as 'sort_key' when sorting items via built-in sort() function.
    Sorts items as ascending based on tags value.

    :param tag_name: str - key linking to a value that will be taken into account when sorting items
    """

    def __init__(self, tag_name: str):
        self.tag_name = tag_name

    def __call__(self, search_result: SearchResult):
        if isinstance(search_result, SearchResult):
            item_ref = search_result.item_ref
            value = item_ref.tags.get(self.tag_name, 9999)
        else:
            print(search_result.tags)
            value = search_result.tags.get(self.tag_name, 9999)
            print(value)
        return self._normalize_arg(value)

    def _normalize_arg(self, arg: str):
        if isinstance(arg, str):
            if arg.isdigit():
                return int(arg)

            if arg.isdecimal():
                return float(arg)

        return arg
