import pytest


ARGV_CREATE_CONTAINER = ['', 'create', 'container', 'test', '8', '8']


@pytest.fixture
def argv_create_container() -> list[str]:
    return ARGV_CREATE_CONTAINER
