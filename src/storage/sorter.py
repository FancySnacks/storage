"""Sorts list of SearchResults instances in specific order via given key"""

from storage.search import SearchResult


class Sorter:

    def __call__(self, search_result: SearchResult):
        return search_result.len_of_matches()
