import pytest

from storage.cli.exceptions import DuplicateNameError, NoFreeSpacesError, ItemIsNotEmptyError


def test_drawer_is_added_to_container(container, test_drawer_name):
    container.add_drawer(test_drawer_name)
    assert len(container.drawers) == 1


def test_container_is_resized(container):
    prev_total = container.get_max_drawer_count
    container.resize_container(1, 2)
    new_total = container.get_max_drawer_count
    assert prev_total != new_total


def test_duplicate_drawer_not_added(container, test_drawer_name):
    with pytest.raises(DuplicateNameError):
        container.add_drawer(test_drawer_name)
        container.add_drawer(test_drawer_name)


def test_new_drawer_not_added_when_row_is_full(container, test_drawer_name):
    with pytest.raises(NoFreeSpacesError):
        container.add_drawer(test_drawer_name)
        container.resize_container(1, 1)
        container.add_drawer("secondtestDrawer")


def test_drawer_is_moved_to_another_spot(container, test_drawer_name):
    drawer = container.add_drawer(test_drawer_name)
    old_pos = drawer.position
    container.move_drawer_to(drawer, 1, 5)
    new_pos = container.get_drawer_by_name(test_drawer_name).position
    assert old_pos != new_pos and container.get_drawer_at_pos(old_pos[0], old_pos[1]) != drawer


def test_drawer_is_removed_from_container_at_pos(container, test_drawer_name):
    container.add_drawer(test_drawer_name)
    container.remove_drawer_at_pos(0, 0)
    target_row = container.drawer_rows[0]
    assert target_row.is_column_free(0) is True


def test_drawer_is_removed_from_container_via_name(container, test_drawer_name):
    container.add_drawer(test_drawer_name)
    container.remove_drawer_by_name(test_drawer_name)
    assert len(container.drawers) == 0


def test_non_empty_drawer_cannot_be_removed_from_container(container, test_drawer_name, component_dict):
    with pytest.raises(ItemIsNotEmptyError):
        drawer = container.add_drawer(test_drawer_name)
        drawer.add_component(**component_dict)
        container.remove_drawer_by_name(test_drawer_name)


def test_container_is_cleared(container, test_drawer_name):
    container.add_drawer(test_drawer_name)
    container.clear_container()
    assert len(container.drawers) == 0
