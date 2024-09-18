import pytest


def test_drawer_is_added_to_container(container, test_drawer_name):
    container.add_drawer(test_drawer_name)
    assert len(container.drawers) == 1


def test_container_is_resized(container):
    prev_total = container.get_max_drawer_count
    container.resize_container(1, 2)
    new_total = container.get_max_drawer_count
    assert prev_total != new_total


def test_duplicate_drawer_not_added(container, test_drawer_name):
    container.add_drawer(test_drawer_name)
    container.add_drawer(test_drawer_name)
    assert len(container.drawers) != 2


def test_new_drawer_not_added_when_row_is_full(container, test_drawer_name):
    with pytest.raises(IndexError):
        container.resize_container(1, 1)
        container.add_drawer(test_drawer_name)
        container.get_next_free_row_and_column()


def test_drawer_is_removed_from_container_at_pos(container):
    container.remove_drawer_at_pos(0, 0)
    assert len(container.drawers) == 0


def test_drawer_is_removed_from_container_via_name(container, test_drawer_name):
    container.add_drawer(test_drawer_name)
    container.remove_drawer_by_name(test_drawer_name)
    assert len(container.drawers) == 0


def test_container_is_cleared(container, test_drawer_name):
    container.add_drawer(test_drawer_name)
    container.clear_container()
    assert len(container.drawers) == 0
