import pytest

from storage.cli.exceptions import ContainerNotFoundError, ItemNotFoundError


def test_create_new_container(session, container_dict):
    session.create_container(**container_dict)


def test_create_new_drawer(session, container_dict, drawer_dict):
    session.create_container(**container_dict)
    session.create_drawer(**drawer_dict)


def test_create_new_component(session, container_dict, drawer_dict, component_dict):
    session.create_container(**container_dict)
    session.create_drawer(**drawer_dict)
    session.create_component(**component_dict, parent_drawer_name=drawer_dict['name'],
                             parent_container_name=container_dict['name'])


def test_raises_container_not_found_exception(session):
    with pytest.raises(ContainerNotFoundError):
        session.get_container_by_name('InvalidName')


def test_raises_drawer_not_found_exception(session, container):
    with pytest.raises(ItemNotFoundError):
        session.containers.append(container)
        session.get_drawer_by_name('InvalidName', container.name)
