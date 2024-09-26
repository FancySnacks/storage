import pytest

from storage.cli.argexecutor import CreateArgExecutor, DeleteArgExecutor
from storage.session import Session


a = Session()


@pytest.fixture
def s():
    return a


def test_new_container_created(argv_create_container, s):
    executor = CreateArgExecutor(s, argv_create_container)
    executor.parse_args()

    assert len(s.containers) > 0


def test_new_drawer_created(argv_create_drawer, s):
    executor = CreateArgExecutor(s, argv_create_drawer)
    executor.parse_args()
    print(s.containers)

    assert len(s.containers[-1].drawers) > 0


def test_new_component_created(argv_create_component, s):
    executor = CreateArgExecutor(s, argv_create_component)
    executor.parse_args()

    assert len(s.containers[-1].drawers[-1].components) > 0


def test_component_deleted(argv_delete_component, s):
    executor = DeleteArgExecutor(s, argv_delete_component)
    executor.parse_args()

    assert len(s.get_drawer_by_name('testDrawer', 'testContainer').components) == 0


def test_drawer_deleted(argv_delete_drawer, s):
    executor = DeleteArgExecutor(s, argv_delete_drawer)
    executor.parse_args()

    assert len(s.get_container_by_name('testContainer').drawers) == 0
