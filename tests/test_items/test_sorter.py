import pytest

from storage.search import SearchQuery, Searcher, SearchMode
from storage.sorter import sort_items


@pytest.fixture
def second_component() -> dict:
    return {'name': 'secondComponent', 'count': 0, 'type': 'other', 'tags': {}}


def test_components_are_sorted_by_tag_matches(container_complete, second_component):
    container_complete.drawers[0].add_component(**second_component)
    unsorted_comps = container_complete.get_all_components()

    query = SearchQuery(SearchMode.ANY)
    searcher = Searcher(query, unsorted_comps)

    search_results = searcher.search_through_items(['other'], {}, ["count<1"])
    sorted_comps = sort_items(search_results.copy(), 'accuracy')

    assert sorted_comps != unsorted_comps


def test_components_are_sorted_by_count(container_complete, second_component):
    container_complete.drawers[0].add_component(**second_component)

    unsorted_comps = container_complete.get_all_components()
    sorted_comps = sort_items(unsorted_comps.copy(), 'count')

    assert sorted_comps != unsorted_comps


def test_components_are_sorted_by_name(container_complete, second_component):
    container_complete.drawers[0].add_component(**second_component)

    unsorted_comps = container_complete.get_all_components()
    sorted_comps = sort_items(unsorted_comps.copy(), 'name')

    assert sorted_comps != unsorted_comps


def test_components_can_be_sorted_in_reverse(container_complete, second_component):
    container_complete.drawers[0].add_component(**second_component)

    unsorted_comps = container_complete.get_all_components()
    sorted_comps = sort_items(unsorted_comps.copy(), 'name', reverse=True)

    assert sorted_comps != unsorted_comps
