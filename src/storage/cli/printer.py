class Printer:
    messages = {"ADD_SUCCESS": {1: "'{name}' {item} was created",
                                2: "'{name}' {item} was added to '{relation}'",
                                3: "'{name}' {item} was added to '{relation}' at {pos}"},
                "ADD_FAIL": {1: "'{name}' {item} could not be created",
                             2: "'{name}' {item} could not be added to '{relation}' {reason}"},
                "ADD_FAIL_NO_SPOTS": {1: "New {item} could not be created",
                                      2: "New {item} could not be added to '{relation}' {reason}"},
                "ADD_FAIL_SPOT_TAKEN": {1: "New {item} could not be created",
                                        2: "New {item} could not be added to '{relation}' at {pos} {reason}"},
                "DEL_SUCCESS": {1: "'{name}' {item} was deleted",
                                2: "'{name}' {item} was removed from '{relation}'",
                                3: "'{name}' {item} was removed from '{relation}' at {pos}"},
                "DEL_FAIL": {1: "'{name}' {item} could not be deleted",
                             2: "'{name}' {item} could not be removed from '{relation}' {reason}",
                             3: "'{name}' {item} could not be removed from '{relation}' at {pos} {reason}"},
                "DEL_FAIL_CONTAINER": {1: "'{name}' {item} could not be removed",
                                       2: "'{name}' {item} could not be removed {reason}"},
                "CLEAR_SUCCESS": {1: "'{name}' {item} was cleared from children",
                                  2: "'{name}' {item} at {pos} was cleared from children"},
                "ITEM_NOT_FOUND_NAME": {1: "'{name}' {item} was not found",
                                        2: "'{name}' {item} was not found inside '{relation}'"},
                "CONTAINER_NOT_FOUND": {1: "'{name}' container does not exist"},
                "ITEM_NOT_FOUND_POS": {1: "{item} was not found",
                                       2: "{item} was not found inside '{relation}' at position {pos}"}
                }

    @classmethod
    def get_message(cls, key: str, verbosity: int = 1, **kwargs) -> str:
        verbosity = min(cls.get_max_verbosity_level_possible(key), verbosity)
        message = cls.messages.get(key)[verbosity]
        return message.format(**kwargs)

    @classmethod
    def get_max_verbosity_level_possible(cls, key: str) -> int:
        message_verbosity_levels = cls.messages.get(key).keys()
        min_level = [int(level_key) for level_key in message_verbosity_levels]
        return max(min_level)
