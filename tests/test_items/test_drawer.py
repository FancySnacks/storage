import pytest

from storage.cli.exceptions import DuplicateNameError, NoFreeSpacesError


def test_component_is_added_to_drawer(drawer, component_dict):
    drawer.add_component(**component_dict)
    assert len(drawer.components) == 1


def test_duplicate_component_not_added(drawer, component_dict):
    with pytest.raises(DuplicateNameError):
        drawer.add_component(**component_dict)
        drawer.add_component(**component_dict)


def test_new_component_not_added_when_drawer_is_full(drawer, component_dict):
    with pytest.raises(NoFreeSpacesError):
        drawer.parent_container.compartments_per_drawer = 0
        drawer.add_component(**component_dict)


def test_component_is_removed_from_drawer_via_name(drawer, component_dict, test_component_name):
    drawer.add_component(**component_dict)
    drawer.remove_component_by_name(test_component_name)
    assert len(drawer.components) == 0


def test_component_is_removed_from_drawer_via_index(drawer, component_dict):
    drawer.add_component(**component_dict)
    drawer.remove_component_by_index(0)
    assert len(drawer.components) == 0


def test_drawer_is_cleared(drawer, component_dict):
    drawer.add_component(**component_dict)
    drawer.clear_drawer()
    assert len(drawer.components) == 0
