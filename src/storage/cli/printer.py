import json
import pathlib

from storage.util import json_digit_string_keys_to_ints


PRINTER_MESSAGES_PATH = pathlib.Path.cwd().joinpath('./config/console_messages.json')


def load_console_messages_from_file(filepath=PRINTER_MESSAGES_PATH):
    with open(filepath, 'r') as f:
        json_data = json.load(f)
        json_data = json_digit_string_keys_to_ints(json_data)

    return json_data


class Printer:
    messages: dict = load_console_messages_from_file()
    silent: bool = False
    exceptions_ignore_silent_mode: bool = True

    @classmethod
    def get_message(cls, key: str, verbosity: int = 1, is_exception: bool = False, **kwargs) -> str:
        if cls.silent and not is_exception:
            return ""

        verbosity = min(cls.get_max_verbosity_level_possible(key), verbosity)
        message = cls.messages.get(key)[verbosity]
        return message.format(**kwargs)

    @classmethod
    def get_max_verbosity_level_possible(cls, key: str) -> int:
        message_verbosity_levels = cls.messages.get(key).keys()
        min_level = [int(level_key) for level_key in message_verbosity_levels]
        return max(min_level)
