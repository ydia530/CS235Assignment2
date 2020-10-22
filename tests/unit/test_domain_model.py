from datetime import date

import pytest

from CS235flix.adapters.MemoryRepository import make_review
from CS235flix.domain.model import User, Movie, Review, Genre


@pytest.fixture()
def movie():
    return Movie("Guardians of the Galaxy", 2014)


@pytest.fixture()
def user():
    return User('ydia530', '12345QWE')


@pytest.fixture()
def genre():
    return Genre('Action')


def test_user_construction(user):
    assert user.user_name == 'ydia530'
    assert user.password == '12345QWE'
    assert repr(user) == '<User ydia530>'

    for review in user.reviews:
        # User should have an empty list of reviews after construction.
        assert False


def test_movie_construction(movie):
    assert movie.rank is None
    assert movie.release_year == 2014
    assert movie.title == 'Guardians of the Galaxy'
    assert len(movie.reviews) == 0
    assert len(movie.genres) == 0

    assert repr(
        movie) == '<Movie Guardians of the Galaxy, 2014>'


def test_movie_comparison():
    movie1 = Movie("a", 2012)
    movie2 = Movie("a", 2011)
    assert movie2 < movie1


def test_genre_construction(genre):
    assert genre.genre_name == "Action"

    for movie in genre.genre_movies:
        assert False
    assert not genre.is_applied_to(Movie("a", 2014))


def test_make_review_relationships(movie, user):
    review_text = "This is a nice Movie"
    review = make_review(review_text, movie, user, date.today())

    assert review in user.reviews

    assert review.user == user

    assert review in movie.reviews

    assert review.movie is movie
