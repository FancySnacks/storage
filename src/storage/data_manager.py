"""DataManager class handles loading and saving data to file as well as synchronisation."""

from abc import ABC, abstractmethod


class DataManager(ABC):
    # TODO: allowed formats: json, yaml, sql
    @abstractmethod
    def load_data_from_file(self) -> dict:
        pass

    @abstractmethod
    def save_data_to_file(self) -> dict:
        pass
