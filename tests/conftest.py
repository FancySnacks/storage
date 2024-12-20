import pytest

from storage.session import Session
from storage.items.container import Container
from storage.items.drawer import Drawer


@pytest.fixture
def session() -> Session:
    return Session()


TEST_CONTAINER_NAME = 'testContainer'
TEST_DRAWER_NAME = 'testDrawer'
TEST_COMPONENT_NAME = 'testComponent'


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
def container(test_container_name) -> Container:
    return Container(name=TEST_CONTAINER_NAME, total_rows=8, max_drawers_per_row=8, compartments_per_drawer=3)


@pytest.fixture
def container_dict() -> dict:
    return {'name': TEST_CONTAINER_NAME, 'rows': 8, 'columns': 8}


@pytest.fixture
def drawer(container) -> Drawer:
    return Drawer(name=TEST_DRAWER_NAME, row=0, column=0, parent_container=container)


@pytest.fixture
def drawer_dict() -> dict:
    return {'name': TEST_DRAWER_NAME, 'row': 0, 'column': 0, 'container': TEST_CONTAINER_NAME}


@pytest.fixture
def component_dict() -> dict:
    return {'name': TEST_COMPONENT_NAME, 'count': 1, 'type': 'other', 'tags': {}}


@pytest.fixture
def container_complete(component_dict) -> Container:
    c = Container(name=TEST_CONTAINER_NAME, total_rows=8, max_drawers_per_row=8, compartments_per_drawer=3)
    d = c.add_drawer(TEST_DRAWER_NAME)
    d.add_component(**component_dict)
    return c
