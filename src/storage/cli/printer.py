
class Printer:
    messages = {"ADD_SUCCESS": {1: "'{name}' {item} was added to '{relation}'",
                                2: "'{name}' {item} was added to '{relation}' at position {pos}",
                                3: "3"},
                }

    @classmethod
    def get_message(cls, key: str, verbosity: int = 1, **kwargs) -> str:
        message = cls.messages.get(key)[verbosity]
        return message.format(**kwargs)

p = Printer.get_message("ADD_SUCCESS", name='hello', item='container', relation='')
print(p)