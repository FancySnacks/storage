import pytest

from storage.cli.argexecutor import CreateArgExecutor, DeleteArgExecutor
from storage.cli.exceptions import ContainerNotFoundError, ItemNotFoundError


def test_new_container_created(argv_create_container, executor_session):
    executor = CreateArgExecutor(executor_session, argv_create_container)
    executor.parse_args()

    assert len(executor_session.containers) > 0


def test_new_drawer_created(argv_create_drawer, executor_session):
    executor = CreateArgExecutor(executor_session, argv_create_drawer)
    executor.parse_args()

    assert len(executor_session.containers[-1].drawers) > 0


def test_new_component_created(argv_create_component, executor_session):
    executor = CreateArgExecutor(executor_session, argv_create_component)
    executor.parse_args()

    assert len(executor_session.containers[-1].drawers[-1].components) > 0


def test_component_deleted(argv_delete_component, executor_session):
    executor = DeleteArgExecutor(executor_session, argv_delete_component)
    executor.parse_args()

    assert len(executor_session.get_drawer_by_name('testDrawer', 'testContainer').components) == 0


def test_drawer_deleted(argv_delete_drawer, executor_session):
    with pytest.raises(ItemNotFoundError):
        executor = DeleteArgExecutor(executor_session, argv_delete_drawer)
        executor.parse_args()
        executor_session.get_drawer_by_name('testDrawer', 'testContainer')


def test_container_deleted(argv_delete_container, executor_session):
    with pytest.raises(ContainerNotFoundError):
        executor = DeleteArgExecutor(executor_session, argv_delete_container)
        executor.parse_args()
        executor_session.get_container_by_name('testContainer')
