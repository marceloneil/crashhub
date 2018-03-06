import os
import pytest

ROOT_DIR = os.path.dirname(__file__)

def pytest_addoption(parser):
    parser.addoption(
        '--db',
        action='append',
        default=['sqlite'],
        help='comma seperated databases to test'
    )

def pytest_generate_tests(metafunc):
    if 'crashhub_client' in metafunc.fixturenames:
        dbs = metafunc.config.getoption('db')
        metafunc.parametrize('crashhub_client', dbs, indirect=True)


@pytest.fixture
def crashhub_client(tmpdir, mocker, request):
    mocker.patch("github.Github")

    os.chdir(ROOT_DIR + "/tests/" + request.param)
    mocker.patch("lib.config.read_config")
    os.chdir(ROOT_DIR)

    if request.param == "sqlite":
        from lib import config
        config.config["db_name"] = "{}/db.sqlite3".format(tmpdir)

    from crashhub import app
    from lib import database
    app.testing = True
    client = app.test_client()
    with app.app_context():
        database.create_tables()

    return client
