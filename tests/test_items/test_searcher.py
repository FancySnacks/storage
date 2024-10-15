import pytest

from storage.const import SearchMode
from storage.search import SearchQuery, Searcher


@pytest.fixture
def second_component() -> dict:
    return {'name': 'secondComponent', 'count': 0, 'type': 'other', 'tags': {}}


def test_no_components_on_empty_tags(container_complete, second_component):
    container_complete.drawers[0].add_component(**second_component)
    unsorted_comps = container_complete.get_all_components()

    query = SearchQuery(SearchMode.ANY)
    searcher = Searcher(query, unsorted_comps)

    search_results = searcher.search_through_items([], {}, [])

    assert len(search_results) == 0


def test_search_components_any(container_complete, second_component):
    container_complete.drawers[0].add_component(**second_component)
    unsorted_comps = container_complete.get_all_components()

    query = SearchQuery(SearchMode.ANY)
    searcher = Searcher(query, unsorted_comps)

    search_results = searcher.search_through_items(['other'], {}, [])

    assert len(search_results) == 2


def test_search_components_all(container_complete, second_component):
    container_complete.drawers[0].add_component(**second_component)
    unsorted_comps = container_complete.get_all_components()

    query = SearchQuery(SearchMode.ALL)
    searcher = Searcher(query, unsorted_comps)

    search_results = searcher.search_through_items([], {"name": "secondComponent"}, [])

    assert len(search_results) == 1
