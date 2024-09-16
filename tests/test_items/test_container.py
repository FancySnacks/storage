def test_drawer_is_added_to_container(container, test_drawer_name):
    container.add_drawer(test_drawer_name)
    assert len(container.drawers) == 1


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
