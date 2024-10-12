
class Printer:
    messages = {"ADD_SUCCESS": {1: "'{name}' {item} was created",
                                2: "'{name}' {item} was added to '{relation}'",
                                3: "'{name}' {item} was added to '{relation}' at position {pos}"},
                }

    @classmethod
    def get_message(cls, key: str, verbosity: int = 1, **kwargs) -> str:
        verbosity = min(verbosity, 3)
        message = cls.messages.get(key)[verbosity]
        return message.format(**kwargs)
