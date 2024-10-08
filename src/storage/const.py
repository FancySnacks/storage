"""Constant variables, classes and functions"""

from __future__ import annotations

import pathlib

from typing import Union, Any, NewType
from enum import StrEnum, auto

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
DICT_ITEMS = NewType('dict_items', list[tuple[str, Any]])


class SearchMode(StrEnum):
    ANY = auto()
    ALL = auto()


class ComponentType(StrEnum):
    RESISTOR = auto()
    CAPACITOR = auto()
    DIODE = auto()
    INDUCTOR = auto()
    TRANSISTOR = auto()
    IC = auto()
    MICROCONTROLLER = auto()
    OTHER = auto()


def create_component_type_enum_from_file() -> dict:
    with open(COMPONENT_TYPE_CONFIG_PATH, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return {line.upper(): line for line in lines}


def get_component_types(enum_class) -> list[str]:
    names = enum_class.__members__.keys()
    return [name.lower() for name in names]


ComponentType = StrEnum('DynamicEnum', create_component_type_enum_from_file())
