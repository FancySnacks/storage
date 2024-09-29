import pytest

import pathlib

from storage.cli.parser import ArgParser
from storage.cli.subparser import CreateSubparser, GetSubparser, DeleteSubparser, ClearSubparser
from storage.session import Session


s = Session()


@pytest.fixture
def executor_session() -> Session:
    return s


arg_parser = ArgParser()

arg_parser.add_subparser(CreateSubparser(arg_parser))
arg_parser.add_subparser(GetSubparser(arg_parser))
arg_parser.add_subparser(DeleteSubparser(arg_parser))
arg_parser.add_subparser(ClearSubparser(arg_parser))

arg_parser.setup_args()


@pytest.fixture
def parser() -> ArgParser:
    return arg_parser


create_args_path = pathlib.Path(__file__).parent.joinpath('./create_args.txt')
delete_args_path = pathlib.Path(__file__).parent.joinpath('./delete_args.txt')
clear_args_path = pathlib.Path(__file__).parent.joinpath('./clear_args.txt')

with open(create_args_path, 'r') as f:
    create_args: list[str] = f.readlines()
    create_args = [line.replace(" ", ",").replace("\n", "").replace('"', "") for line in create_args]

with open(delete_args_path, 'r') as f:
    delete_args: list[str] = f.readlines()
    delete_args = [line.replace(" ", ",").replace("\n", "").replace('"', "") for line in delete_args]

with open(clear_args_path, 'r') as f:
    clear_args: list[str] = f.readlines()
    clear_args = [line.replace(" ", ",").replace("\n", "").replace('"', "") for line in clear_args]


ARGV_CREATE_CONTAINER = create_args[0].split(',')
ARGV_CREATE_DRAWER = create_args[1].split(',')
ARGV_CREATE_COMPONENT = create_args[2].split(',')

ARGV_DELETE_CONTAINER = delete_args[2].split(',')
ARGV_DELETE_DRAWER = delete_args[1].split(',')
ARGV_DELETE_COMPONENT = delete_args[0].split(',')

ARGV_CLEAR_CONTAINER = clear_args[1].split(',')
ARGV_CLEAR_DRAWER = clear_args[0].split(',')


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
