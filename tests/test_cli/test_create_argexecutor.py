from storage.cli.argexecutor import CreateArgExecutor


def test_new_container_dir_created(argv_create_container, session):
    executor = CreateArgExecutor(session, argv_create_container)
