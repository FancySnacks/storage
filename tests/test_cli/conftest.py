import pytest

import pathlib


create_args_path = pathlib.Path(__file__).parent.joinpath('./create_args.txt')

with open(create_args_path, 'r') as f:
    create_args = f.readlines()
    create_args = [line.replace('\n', '') for line in create_args]
    create_args = [line.split(',') for line in create_args]


ARGV_CREATE_CONTAINER = create_args[0]
ARGV_CREATE_DRAWER = create_args[1]
ARGV_CREATE_COMPONENT = create_args[2]


@pytest.fixture
def argv_create_container() -> list[str]:
    return ARGV_CREATE_CONTAINER


@pytest.fixture
def argv_create_drawer() -> list[str]:
    return ARGV_CREATE_DRAWER


@pytest.fixture
def argv_create_component() -> list[str]:
    return ARGV_CREATE_COMPONENT
