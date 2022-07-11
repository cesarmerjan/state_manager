from src.database.interfaces import DatabaseManagerInterface


def get_mocked_database_manager():
    def _disconnect(self):
        self.connection_pool = None

    def _connect(self, *args, **kwargs):
        self.connection_pool = True

    DatabaseManager = type(
        "UnitOfWork",
        (DatabaseManagerInterface,),
        {
            "is_connected": lambda: True,
            "_make_connection_pool": lambda self, username, password: True,
            "_get_database_client": lambda: None,
            "_database_client_factory": lambda: None,
            "_disconnect": _disconnect,
            "_connect": _connect
        },
    )

    return DatabaseManager()


def test_database_manager_connect():
    database_manager = get_mocked_database_manager()

    database_manager.connect()

    assert database_manager.is_connected


def test_database_manager_disconnect():
    database_manager = get_mocked_database_manager()

    database_manager.disconnect()

    assert database_manager.is_connected
