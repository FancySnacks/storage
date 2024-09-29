import pathlib

from storage.data_manager import JSONDataManager


def test_container_is_saved_to_file(tmp_path, container):
    data_manager = JSONDataManager()
    data_manager.container_path = tmp_path
    data_manager.save_data_to_file(container)
    file_path = pathlib.Path(tmp_path).joinpath(data_manager.create_filepath(container))

    assert file_path.exists() is True


def test_container_file_is_updated(tmp_path, container, drawer_dict):
    drawer_dict.pop('container')

    data_manager = JSONDataManager()
    data_manager.container_path = tmp_path
    data_manager.save_data_to_file(container)
    file_path = pathlib.Path(tmp_path).joinpath(data_manager.create_filepath(container))
    drawers_a = container.drawers.copy()

    container.add_drawer(**drawer_dict)
    data_manager.save_data_to_file(container)

    container_new = data_manager.load_data_from_file(file_path)

    assert len(drawers_a) != len(container_new.get('drawers'))


def test_container_file_is_deleted(tmp_path, container):
    data_manager = JSONDataManager()
    data_manager.container_path = tmp_path
    data_manager.save_data_to_file(container)
    file_path = pathlib.Path(tmp_path).joinpath(data_manager.create_filepath(container))
    data_manager.delete_container_file(container.name)

    assert file_path.exists() is False
