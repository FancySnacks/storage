"""Search and filter items through positional and keyword tags"""

from dataclasses import dataclass, field
from typing import Callable

from storage.const import SearchMode, ITEM, DICT_ITEMS
from storage.util import split_op_value_into_strings, split_range_value_into_strings


@dataclass
class SearchQuery:
    tags_positionals: list[str] = field(init=False, default_factory=list)
    tags_keywords: dict = field(init=False, default_factory=dict)
    mode: SearchMode


@dataclass
class SearchResult:
    item_ref: ITEM
    matched_positionals: list[str] = field(init=False, default_factory=list)
    matched_keywords: dict = field(init=False, default_factory=dict)
    matched_comparisons: dict = field(init=False, default_factory=dict)
    query: SearchQuery

    def len_of_matches(self) -> int:
        return len(self.matched_positionals) + len(self.matched_keywords) + len(self.matched_comparisons)

    def __repr__(self) -> str:
        return f"{self.item_ref.get_location_readable_format()} (Matched Tags: {self.len_of_matches()})"


class Searcher:
    def __init__(self, query: SearchQuery, items: list[ITEM]):
        self.query = query
        self.items = items

    def search_through_items(self, tags_positionals: list[str], tags_keywords: dict,
                             tags_comparison: list[str]) -> list:
        valid_items = []

        for item in self.items:
            search_result = None
            vals = item.tags.items()

            keyword_matches = self.get_matching_keywords(vals, tags_keywords)
            positional_matches = self.get_matching_positionals(vals, tags_positionals)
            comparison_matches = self.get_matching_comparisons(vals, tags_comparison)

            if self.query.mode == SearchMode.ANY:
                if any((keyword_matches, positional_matches, comparison_matches)):
                    search_result = SearchResult(item_ref=item, query=self.query)
                    search_result.matched_positionals = positional_matches
                    search_result.matched_keywords = keyword_matches
                    search_result.matched_comparisons = comparison_matches
            elif self.query.mode == SearchMode.ALL:
                search_result = SearchResult(item_ref=item, query=self.query)
                search_result.matched_positionals = positional_matches
                search_result.matched_keywords = keyword_matches
                search_result.matched_comparisons = comparison_matches

                if not self.all_tags_matched(search_result, tags_positionals, tags_keywords, comparison_matches):
                    search_result = None

            if search_result:
                valid_items.append(search_result)

        return valid_items

    def get_matching_keywords(self, item_tags: DICT_ITEMS, tags_keywords: dict) -> dict:
        """Return shared tags between item_tags (dict_items) and passed tags_keywords arg (dict)"""
        tags_keywords = self._normalize_dict_values(tags_keywords)
        return {item[0]: item[1] for item in item_tags
                if item in tags_keywords.items()}

    def get_matching_positionals(self, item_tags: DICT_ITEMS, tags_positionals: list[str]) -> list[str]:
        """Return a list of shared strings (key or value) between the item_tags (dict_items)
        and tags_positionals (list[str])"""
        matched_positionals: list[str] = []

        for k, v in item_tags:
            k = str(k)
            v = str(v)

            if k in tags_positionals:
                matched_positionals.append(k)

            elif v in tags_positionals:
                matched_positionals.append(v)

        return matched_positionals

    def get_matching_comparisons(self, item_tags: DICT_ITEMS, tags_comparison: list[str]) -> list[str]:
        """Return a list of shared strings (key or value) between the item_tags (dict_items)
        and tags_positionals (list[str])"""
        matched_comparisons: list[str] = []

        for item in item_tags:
            for tag in tags_comparison:
                key, value, operator = split_op_value_into_strings(tag)
                item_key, item_val = item[0], item[1]

                if item_key == key:
                    op_handler = OperatorHandler()

                    if '-' in value:
                        range_a, range_b = split_range_value_into_strings(value)
                        match = op_handler.get_result('-', item_val, range_a, range_b)
                    else:
                        match = op_handler.get_result(operator, item_val, value)

                    if match:
                        matched_comparisons.append(tag)

        return matched_comparisons

    def all_tags_matched(self, search_result: SearchResult, positional_tags: list[str], keyword_tags: dict,
                         comparison_tags: list[str]) -> bool:

        all_positionals_matched: bool = len(search_result.matched_positionals) == len(positional_tags)
        all_keywords_matched: bool = len(search_result.matched_keywords) == len(keyword_tags)
        all_comparisons_matched: bool = len(search_result.matched_comparisons) == len(comparison_tags)

        return all_positionals_matched + all_keywords_matched + all_comparisons_matched > 1

    def _normalize_dict_values(self, tags_keywords: dict) -> dict:
        """Turn any occurring digit string values into actual ints"""
        for k, v in tags_keywords.items():
            try:
                if v.isdigit():
                    tags_keywords[k] = int(v)
            except AttributeError:
                continue

        return tags_keywords


class OperatorHandler:
    def __init__(self):
        self.op_mapping = {"<": self.lesser,
                           ">": self.greater,
                           "<=": self.lesser_or_equal,
                           ">=": self.greater_or_equal,
                           '-': self.in_range}

    def get_result(self, operator: str, *args) -> bool:
        comparison_func: Callable = self.op_mapping.get(operator)
        return comparison_func(*args)

    def lesser(self, val, other_val) -> bool:
        return val < other_val

    def greater(self, val, other_val) -> bool:
        return val > other_val

    def lesser_or_equal(self, val, other_val) -> bool:
        return val <= other_val

    def greater_or_equal(self, val, other_val) -> bool:
        return val >= other_val

    def in_range(self, val, range_a: int, range_b) -> bool:
        return val in range(range_a, range_b+1)
