import os
import pytest

from CS235flix import create_app

from CS235flix.adapters import MemoryRepository
from CS235flix.adapters.MemoryRepository import memoryRepository, populate

TEST_DATA_PATH = os.path.join('/Users', 'diaoyuan', 'Desktop', '235', 'CS235Assignment2', 'tests', 'data')
#TEST_DATA_PATH = "/Users/diaoyuan/Desktop/235/CS235Assignment2/tests/data"

@pytest.fixture
def in_memory_repo():
    repo = memoryRepository()
    populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,  # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False  # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='ydia530', password='12345QWE'):
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
