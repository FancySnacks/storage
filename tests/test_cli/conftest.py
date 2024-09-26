import pytest


ARGV_CREATE_CONTAINER = ['', 'create', 'container', 'testContainer', '8', '8']
ARGV_CREATE_DRAWER = ['', 'create', 'drawer', 'testDrawer', 'testContainer']
ARGV_CREATE_COMPONENT = ['', 'create', 'component', 'testComponent', '5', 'other', 'testContainer', 'testDrawer']


@pytest.fixture
def argv_create_container() -> list[str]:
    return ARGV_CREATE_CONTAINER


@pytest.fixture
def argv_create_drawer() -> list[str]:
    return ARGV_CREATE_DRAWER


@pytest.fixture
def argv_create_component() -> list[str]:
    return ARGV_CREATE_COMPONENT
