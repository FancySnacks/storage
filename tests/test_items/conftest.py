import pytest

from storage.items.container import Container
from storage.items.drawer import Drawer


TEST_CONTAINER_NAME = 'TestContainer'
TEST_DRAWER_NAME = 'TestDrawer'
TEST_COMPONENT_NAME = 'TestComponent'


@pytest.fixture
def test_container_name() -> str:
    return TEST_CONTAINER_NAME


@pytest.fixture
def test_drawer_name() -> str:
    return TEST_DRAWER_NAME


@pytest.fixture
def test_component_name() -> str:
    return TEST_COMPONENT_NAME


@pytest.fixture
def container() -> Container:
    return Container(name=TEST_CONTAINER_NAME, total_rows=8)


@pytest.fixture
def drawer(container) -> Drawer:
    return Drawer(name=TEST_DRAWER_NAME, row=0, column=0, parent_container=container)


@pytest.fixture
def component_dict() -> dict:
    return {'name': TEST_COMPONENT_NAME, 'count': 1, 'type': 'Test', 'tags': {}}
