from storage.cli.printer import Printer


class StorageBaseException(Exception):
    CONSOLE_MESSAGE: str = "This should not happen"
    REASON: str = ""

    def __init__(self, reason: str = "", **metadata):
        self.metadata = dict(**metadata)
        if reason:
            self.REASON = reason

        self.CONSOLE_MESSAGE: str = self.get_formatted_error_msg()
        super().__init__(self.CONSOLE_MESSAGE)

    def get_formatted_error_msg(self) -> str:
        return Printer.get_message(self.CONSOLE_MESSAGE, 2, True, **self.metadata, reason=self.REASON)


# ===== CREATE ===== #

class SpaceOccupiedError(StorageBaseException):
    CONSOLE_MESSAGE: str = "ADD_FAIL_SPOT_TAKEN"
    REASON: str = "as the space is occupied by another"


class NoFreeSpacesError(StorageBaseException):
    CONSOLE_MESSAGE: str = "ADD_FAIL_NO_SPOTS"
    REASON: str = "as there are no more free spots"


class DuplicateNameError(StorageBaseException):
    CONSOLE_MESSAGE = "ADD_FAIL"
    REASON = "as item of the same name already exists"


# ===== GET ===== #

class ItemNotFoundError(StorageBaseException):
    CONSOLE_MESSAGE = "ITEM_NOT_FOUND_NAME"


class ContainerNotFoundError(StorageBaseException):
    CONSOLE_MESSAGE = "CONTAINER_NOT_FOUND"


class ItemNotFoundAtPositionError(StorageBaseException):
    CONSOLE_MESSAGE = "ITEM_NOT_FOUND_POS"


# ===== DELETE ===== #

class ItemIsNotEmptyError(StorageBaseException):
    CONSOLE_MESSAGE = "DEL_FAIL"


class ContainerIsNotEmptyError(StorageBaseException):
    CONSOLE_MESSAGE = "DEL_FAIL_CONTAINER"
