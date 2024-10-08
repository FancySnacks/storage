"""Sorts list of SearchResults instances in specific order via given key"""

from storage.search import SearchResult


class Sorter:
    def __init__(self, search_results: list[SearchResult], sort_key: str = "", reverse=False):
        self.search_results = search_results
        self.sort_key = sort_key
        self.reverse = reverse

    def __call__(self, search_result: SearchResult):
        return search_result.len_of_matches()
