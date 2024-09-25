from enum import StrEnum


class ConsoleMessage(StrEnum):
    ADD_SUCCESS = "'{name}' {item} was added to '{relation}' at position {pos}"
    ADD_FAIL = "'{name}' {item} could not be added to '{relation}' {reason}"
    ADD_FAIL_SPOT_TAKEN = "New {item} could not be added to '{relation}' at {pos} {reason}"
    ADD_FAIL_NO_SPOTS = "New {item} could not be added to '{relation}' {reason}"
    DEL_SUCCESS = "'{name}' {item} was removed from '{relation}'"
    DEL_FAIL = "'{name}' {item} could not be removed from '{relation}' {reason}"
    DEL_FAIL_CONTAINER = "'{name}' {item} could not be removed {reason}"
    ITEM_NOT_FOUND_NAME = "'{name}' {item} was not found inside '{relation}'"
    CONTAINER_NOT_FOUND = "'{name}' container does not exist!"
    ITEM_NOT_FOUND_POS = "{item} was not found inside '{relation}' at position {pos}"
