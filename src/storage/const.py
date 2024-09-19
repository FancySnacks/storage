from enum import StrEnum, auto


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
