import pytest

from storage.cli.argexecutor import CreateArgExecutor, DeleteArgExecutor, ClearArgExecutor
from storage.cli.exceptions import ContainerNotFoundError, ItemNotFoundError


def test_new_container_created(argv_create_container, executor_session, parser):
    args = parser.parse_args(argv_create_container[1::])
    executor = CreateArgExecutor(executor_session, 'container', args)
    executor.parse_args()

    assert len(executor_session.containers) > 0


def test_container_is_cleared(argv_create_drawer, argv_clear_container, executor_session, test_container_name, parser):
    args = parser.parse_args(argv_create_drawer[1::])
    executor = CreateArgExecutor(executor_session, 'drawer', args)
    executor.parse_args()

    args = parser.parse_args(argv_clear_container[1::])
    clear_executor = ClearArgExecutor(executor_session, 'container', args)
    clear_executor.parse_args()
    container = executor_session.get_container_by_name(test_container_name)

    assert len(container.drawers) == 0


def test_new_drawer_created(argv_create_drawer, executor_session, parser):
    args = parser.parse_args(argv_create_drawer[1::])
    executor = CreateArgExecutor(executor_session, 'drawer', args)
    executor.parse_args()

    assert len(executor_session.containers[-1].drawers) > 0


def test_drawer_is_cleared(argv_create_component, argv_clear_drawer, executor_session, test_drawer_name,
                           test_container_name, parser):
    args = parser.parse_args(argv_create_component[1::])
    executor = CreateArgExecutor(executor_session, 'component', args)
    executor.parse_args()

    args = parser.parse_args(argv_clear_drawer[1::])
    clear_executor = ClearArgExecutor(executor_session, 'drawer', args)
    clear_executor.parse_args()
    drawer = executor_session.get_drawer_by_name(test_drawer_name, test_container_name)

    assert len(drawer.components) == 0


def test_new_component_created(argv_create_component, executor_session, parser):
    args = parser.parse_args(argv_create_component[1::])
    executor = CreateArgExecutor(executor_session, 'component', args)
    executor.parse_args()

    assert len(executor_session.containers[-1].drawers[-1].components) > 0


def test_component_deleted(argv_delete_component, executor_session, test_drawer_name, test_container_name, parser):
    args = parser.parse_args(argv_delete_component[1::])
    executor = DeleteArgExecutor(executor_session, 'component', args)
    executor.parse_args()

    assert len(executor_session.get_drawer_by_name(test_drawer_name, test_container_name).components) == 0


def test_drawer_deleted(argv_delete_drawer, executor_session, test_drawer_name, test_container_name, parser):
    with pytest.raises(ItemNotFoundError):
        args = parser.parse_args(argv_delete_drawer[1::])
        executor = DeleteArgExecutor(executor_session, 'drawer', args)
        executor.parse_args()
        executor_session.get_drawer_by_name(test_drawer_name, test_container_name)


def test_container_deleted(argv_delete_container, executor_session, test_container_name, parser):
    with pytest.raises(ContainerNotFoundError):
        args = parser.parse_args(argv_delete_container[1::])
        executor = DeleteArgExecutor(executor_session, 'container', args)
        executor.parse_args()
        executor_session.get_container_by_name(test_container_name)
