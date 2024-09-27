import pytest

import pathlib

from storage.session import Session


s = Session()


@pytest.fixture
def executor_session() -> Session:
    return s


create_args_path = pathlib.Path(__file__).parent.joinpath('./create_args.txt')
delete_args_path = pathlib.Path(__file__).parent.joinpath('./delete_args.txt')
clear_args_path = pathlib.Path(__file__).parent.joinpath('./clear_args.txt')

with open(create_args_path, 'r') as f:
    create_args = f.readlines()
    create_args = [line.replace('\n', '') for line in create_args]
    create_args = [line.split(',') for line in create_args]

with open(delete_args_path, 'r') as f:
    delete_args = f.readlines()
    delete_args = [line.replace('\n', '') for line in delete_args]
    delete_args = [line.split(',') for line in delete_args]

with open(clear_args_path, 'r') as f:
    clear_args = f.readlines()
    clear_args = [line.replace('\n', '') for line in clear_args]
    clear_args = [line.split(',') for line in clear_args]


ARGV_CREATE_CONTAINER = create_args[0]
ARGV_CREATE_DRAWER = create_args[1]
ARGV_CREATE_COMPONENT = create_args[2]

ARGV_DELETE_CONTAINER = delete_args[2]
ARGV_DELETE_DRAWER = delete_args[1]
ARGV_DELETE_COMPONENT = delete_args[0]

ARGV_CLEAR_CONTAINER = clear_args[1]
ARGV_CLEAR_DRAWER = clear_args[0]


@pytest.fixture
def argv_create_container() -> list[str]:
    return ARGV_CREATE_CONTAINER


@pytest.fixture
def argv_create_drawer() -> list[str]:
    return ARGV_CREATE_DRAWER


@pytest.fixture
def argv_create_component() -> list[str]:
    return ARGV_CREATE_COMPONENT


@pytest.fixture
def argv_delete_container() -> list[str]:
    return ARGV_DELETE_CONTAINER


@pytest.fixture
def argv_delete_drawer() -> list[str]:
    return ARGV_DELETE_DRAWER


@pytest.fixture
def argv_delete_component() -> list[str]:
    return ARGV_DELETE_COMPONENT


@pytest.fixture
def argv_clear_container() -> list[str]:
    return ARGV_CLEAR_CONTAINER


@pytest.fixture
def argv_clear_drawer() -> list[str]:
    return ARGV_CLEAR_DRAWER
