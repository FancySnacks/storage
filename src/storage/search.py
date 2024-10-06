"""Search and filter items through positional and keyword tags"""

from dataclasses import dataclass, field

from storage.const import SearchMode


@dataclass
class SearchQuery:
    tags_positionals: list[str] = field(init=False, default_factory=list)
    tags_keywords: dict = field(init=False, default_factory=dict)
    mode: SearchMode


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

            keyword_matches = self.get_matching_keywords(vals, tags_keywords)
            positional_matches = self.get_matching_positionals(vals, tags_positionals)

            if self.query.mode == SearchMode.ANY:
                if any((keyword_matches, positional_matches)):
                    search_result = SearchResult(item_ref=item, query=self.query)
                    search_result.matched_positionals = positional_matches
                    search_result.matched_keywords = keyword_matches
            elif self.query.mode == SearchMode.ALL:
                search_result = SearchResult(item_ref=item, query=self.query)
                search_result.matched_positionals = positional_matches
                search_result.matched_keywords = keyword_matches

                if not self.all_tags_matched(search_result, tags_positionals, tags_keywords):
                    search_result = None

            if search_result:
                valid_items.append(search_result)

        return valid_items

    def get_matching_keywords(self, item_tags: list[tuple], tags_keywords: dict) -> dict:
        """Return shared tags between item_tags (dict_items) and passed tags_keywords arg (dict)"""
        tags_keywords = self._normalize_dict_values(tags_keywords)
        return {item[0]: item[1] for item in item_tags if item in tags_keywords.items()}

    def get_matching_positionals(self, item_tags: list[tuple], tags_positionals: list[str]) -> list[str]:
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

    def all_tags_matched(self, search_result, positional_tags: list[str], keyword_tags: dict) -> bool:
        all_positionals_matched: bool = len(search_result.matched_positionals) == len(positional_tags)
        all_keywords_matched: bool = len(search_result.matched_keywords) == len(keyword_tags)
        return all_positionals_matched + all_keywords_matched > 1

    def _normalize_dict_values(self, tags_keywords: dict) -> dict:
        """Turn any occurring digit string values into actual ints"""
        for k, v in tags_keywords.items():
            if v.isdigit():
                tags_keywords[k] = int(v)
        return tags_keywords
