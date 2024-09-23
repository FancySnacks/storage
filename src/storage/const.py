import pathlib

from enum import StrEnum, auto


MODULE_ROOT_PATH = pathlib.Path.cwd()
SAVE_PATH = MODULE_ROOT_PATH.joinpath('save')
CONTAINER_SAVE_PATH = SAVE_PATH.joinpath('containers')


class ComponentType(StrEnum):
    RESISTOR = auto()
    CAPACITOR = auto()
    DIODE = auto()
    INDUCTOR = auto()
    TRANSISTOR = auto()
    IC = auto()
    MICROCONTROLLER = auto()
    OTHER = auto()

    @classmethod
    def get_component_types(cls) -> list[str]:
        names = cls.__members__.keys()
        return [name.lower() for name in names]
