from storage.cli.printer import Printer


class StorageBaseException(Exception):
    CONSOLE_MESSAGE: str = "This should not happen"
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
    CONSOLE_MESSAGE: str = Printer.get_message("ADD_FAIL_SPOT_TAKEN", 2)
    REASON: str = "as the space is occupied by another"


class NoFreeSpacesError(StorageBaseException):
    CONSOLE_MESSAGE: str = Printer.get_message("ADD_FAIL_NO_SPOTS", 2)
    REASON: str = "as there are no more free spots"


class DuplicateNameError(StorageBaseException):
    CONSOLE_MESSAGE = Printer.get_message("ADD_FAIL", 2)
    REASON = "as item of the same name already exists"


# ===== GET ===== #

class ItemNotFoundError(StorageBaseException):
    CONSOLE_MESSAGE = Printer.get_message("ITEM_NOT_FOUND_NAME", 2)


class ContainerNotFoundError(StorageBaseException):
    CONSOLE_MESSAGE = Printer.get_message("CONTAINER_NOT_FOUND", 2)


class ItemNotFoundAtPositionError(StorageBaseException):
    CONSOLE_MESSAGE = Printer.get_message("ITEM_NOT_FOUND_POS", 2)


# ===== DELETE ===== #

class ItemIsNotEmptyError(StorageBaseException):
    CONSOLE_MESSAGE = Printer.get_message("DEL_FAIL", 2)


class ContainerIsNotEmptyError(StorageBaseException):
    CONSOLE_MESSAGE = Printer.get_message("DEL_FAIL_CONTAINER", 2)
