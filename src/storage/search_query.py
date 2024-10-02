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

    def search_through_items(self, items: list, tags_positionals, tags_keywords: dict):
        valid_items = []

        for item in items:
            search_result = None

            keys = item.tags.values()

            for k, v in keys:
                if k in tags_positionals:
                    if not search_result:
                        search_result = SearchResult(item_ref=item, query=self.query)
                    else:
                        search_result.matched_positionals.append(k)

                elif v in tags_positionals:
                    if not search_result:
                        search_result = SearchResult(item_ref=item, query=self.query)
                    else:
                        search_result.matched_positionals.append(v)

            if search_result:
                valid_items.append(item)
