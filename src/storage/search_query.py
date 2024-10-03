from dataclasses import dataclass, field
from typing import Literal


@dataclass
class SearchQuery:
    tags_positionals: list[str] = field(init=False, default_factory=list)
    tags_keywords: dict = field(init=False, default_factory=dict)
    mode: Literal['all', 'any']


@dataclass
class SearchResult:
    item_ref: object
    matched_positionals: list[str] = field(init=False, default_factory=list)
    matched_keywords: dict = field(init=False, default_factory=dict)
    query: SearchQuery


class Searcher:
    def __init__(self, query: SearchQuery):
        self.query = query

    def search_through_items(self, items: list, tags_positionals, tags_keywords: dict) -> list:
        valid_items = []

        for item in items:
            search_result = None

            vals = item.tags.items()

            matches = self.get_matching_keywords(vals, tags_keywords)

            if matches:
                if not search_result:
                    search_result = SearchResult(item_ref=item, query=self.query)
                search_result.matched_keywords = matches

            for k, v in vals:
                k = str(k)
                v = str(v)

                if k in tags_positionals:
                    if not search_result:
                        search_result = SearchResult(item_ref=item, query=self.query)
                    search_result.matched_positionals.append(k)

                elif v in tags_positionals:
                    if not search_result:
                        search_result = SearchResult(item_ref=item, query=self.query)
                    search_result.matched_positionals.append(v)

            if search_result:
                valid_items.append(search_result)

        return valid_items

    def get_matching_keywords(self, items: list[tuple], tags_keywords: dict) -> dict:
        tags_keywords = self._normalize_dict_values(tags_keywords)

        return {item[0]: item[1] for item in items if item in tags_keywords.items()}

    def _normalize_dict_values(self, tags_keywords: dict) -> dict:
        for k, v in tags_keywords.items():
            if v.isdigit():
                tags_keywords[k] = int(v)
        return tags_keywords
