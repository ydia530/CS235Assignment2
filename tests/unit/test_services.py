
import pytest

from CS235flix.authentication.services import AuthenticationException
from CS235flix.movie_blueprint import services as movie_services
from CS235flix.authentication import services as auth_services
from CS235flix.movie_blueprint.services import NonExistentmovieException


def test_can_add_user(in_memory_repo):
    new_username = 'abc'
    new_password = 'Q123'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')

