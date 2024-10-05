import pathlib

from typing import Union
from enum import StrEnum

from storage.items.container import Container
from storage.items.drawer import Drawer
from storage.items.component import Component


MODULE_ROOT_PATH = pathlib.Path.cwd()

# ===== Save Directory ===== #
SAVE_PATH = MODULE_ROOT_PATH.joinpath('save')
CONTAINER_SAVE_PATH = SAVE_PATH.joinpath('containers')

# ===== Config Files ===== #
CONFIG_PATH = MODULE_ROOT_PATH.joinpath('config')
COMPONENT_TYPE_CONFIG_PATH = CONFIG_PATH.joinpath('component_type.txt')


ITEM = Union[Container, Drawer, Component]


def create_component_type_enum_from_file() -> dict:
    with open(COMPONENT_TYPE_CONFIG_PATH, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return {line.upper(): line for line in lines}


def get_component_types(enum_class) -> list[str]:
    names = enum_class.__members__.keys()
    return [name.lower() for name in names]


ComponentType = StrEnum('DynamicEnum', create_component_type_enum_from_file())
