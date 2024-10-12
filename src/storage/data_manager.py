"""DataManager class handles loading and saving data to file as well as synchronisation."""

import json
import os
import pathlib

from abc import ABC, abstractmethod
from typing import Protocol

from storage.const import SAVE_PATH, CONTAINER_SAVE_PATH


class JSONInterface(Protocol):
    name: str

    def to_json(self) -> dict:
        pass


class DataManager(ABC):
    # TODO: allowed formats: json, yaml, sql
    file_suffix: str = ''

    def __init__(self, save_dir_path=SAVE_PATH, container_dir_path=CONTAINER_SAVE_PATH):
        self.save_path = save_dir_path
        self.container_path = container_dir_path

        self.create_save_dir()
        self.create_container_save_dir()

    def create_save_dir(self):
        if not self.save_path.exists():
            os.mkdir(self.save_path)

    def create_container_save_dir(self):
        if not self.container_path.exists():
            os.mkdir(self.container_path)

    def load_all_container_data_from_save_directory(self) -> list[dict]:
        container_files = self._get_list_of_supported_files_in_dir(self.container_path)
        container_data: list[dict] = []

        for file in container_files:
            loaded_data = self.load_data_from_file(file)
            container_data.append(loaded_data)

        return container_data

    @abstractmethod
    def load_data_from_file(self, filepath) -> dict:
        pass

    @abstractmethod
    def save_data_to_file(self, obj_to_save, filepath):
        pass

    def delete_container_file(self, container_name: str):
        path = pathlib.Path(self.container_path).joinpath(f"{container_name}{self.file_suffix}")
        os.remove(path)

    def _get_list_of_supported_files_in_dir(self, dir_path):
        ls = os.listdir(dir_path)
        return [pathlib.Path(CONTAINER_SAVE_PATH).joinpath(file) for file in ls if
                self._file_is_supported_by_manager(file)]

    def _file_is_supported_by_manager(self, filepath) -> bool:
        return pathlib.Path(filepath).suffix == self.file_suffix

    def create_filepath(self, obj):
        return pathlib.Path(self.container_path).joinpath(f"{obj.name}{self.file_suffix}")


class JSONDataManager(DataManager):
    file_suffix: str = '.json'

    def load_data_from_file(self, filepath) -> dict:
        with open(filepath, 'r') as file:
            data = json.load(file)

        return data

    def save_data_to_file(self, obj_to_save: JSONInterface, filepath=None):
        if not filepath:
            filepath = self.create_filepath(obj_to_save)

        with open(filepath, 'w') as file:
            data = obj_to_save.to_json()
            data = json.dumps(data, indent=4)
            file.write(data)
