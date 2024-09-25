from storage.cli.console_message import ConsoleMessage


class StorageBaseException(Exception):
    CONSOLE_MESSAGE: str = ConsoleMessage
    REASON: str = ""

    def __init__(self, reason: str = "", **metadata):
        self.metadata = dict(**metadata)
        if reason:
            self.REASON = reason

        message: str = self.get_formatted_error_msg()
        super().__init__(message)

    def get_formatted_error_msg(self) -> str:
        return self.CONSOLE_MESSAGE.format(**self.metadata, reason=self.REASON)


# ===== CREATE ===== #

class SpaceOccupiedError(StorageBaseException):
    CONSOLE_MESSAGE: str = ConsoleMessage.ADD_FAIL_SPOT_TAKEN
    REASON: str = "as the space is occupied by another"


class NoFreeSpacesError(StorageBaseException):
    CONSOLE_MESSAGE: str = ConsoleMessage.ADD_FAIL_NO_SPOTS
    REASON: str = "as there are no more free spots"


class DuplicateNameError(StorageBaseException):
    CONSOLE_MESSAGE = ConsoleMessage.ADD_FAIL
    REASON = "as item of the same name already exists"


# ===== GET ===== #

class ItemNotFoundError(StorageBaseException):
    CONSOLE_MESSAGE = ConsoleMessage.ITEM_NOT_FOUND_NAME


class ContainerNotFoundError(StorageBaseException):
    CONSOLE_MESSAGE = ConsoleMessage.CONTAINER_NOT_FOUND


class ItemNotFoundAtPositionError(StorageBaseException):
    CONSOLE_MESSAGE = ConsoleMessage.ITEM_NOT_FOUND_POS


# ===== DELETE ===== #

class ItemIsNotEmptyError(StorageBaseException):
    CONSOLE_MESSAGE = ConsoleMessage.DEL_FAIL_CONTAINER
