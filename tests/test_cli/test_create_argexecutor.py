from storage.cli.argexecutor import CreateArgExecutor


def test_new_container_created(argv_create_container, session):
    executor = CreateArgExecutor(session, argv_create_container)
    executor.parse_args()

    assert len(session.containers) > 0


def test_new_drawer_created(argv_create_container, argv_create_drawer, session):
    executor = CreateArgExecutor(session, argv_create_container)
    executor.parse_args()

    executor = CreateArgExecutor(session, argv_create_drawer)
    executor.parse_args()

    assert len(session.containers[-1].drawers) > 0


def test_new_component_created(argv_create_component, argv_create_container, argv_create_drawer, session):
    executor = CreateArgExecutor(session, argv_create_container)
    executor.parse_args()

    executor = CreateArgExecutor(session, argv_create_drawer)
    executor.parse_args()

    executor = CreateArgExecutor(session, argv_create_component)
    executor.parse_args()

    assert len(session.containers[-1].drawers[-1].components) > 0
