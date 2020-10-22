from datetime import date, datetime
from typing import List

import pytest

from CS235flix.adapters.MemoryRepository import make_review
from CS235flix.adapters.repository import RepositoryException
from CS235flix.authentication.services import AuthenticationException
from CS235flix.domain.model import User, Movie, Genre, Review



def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', 'ASVa123456789')
    in_memory_repo.add_user(user)


    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('ydia530')
    assert user == User('ydia530', '12345QWE')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 11 movies.
    assert number_of_movies == 11


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie("abc", 2016)
    movie.rank = 12
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(12) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the movie is reviewed as expected.
    review_one = [review for review in movie.reviews if review.review_text== 'I like this movie'][0]
    review_two = [review for review in movie.reviews if review.review_text == 'This is what I want'][0]
    review_three = [review for review in movie.reviews if review.review_text == 'I am so enjoy watching this movie!'][0]
    assert review_one.user.user_name == "john"
    assert review_two.user.user_name == 'ydia530'
    assert review_three.user.user_name == 'ydia530'



def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(101)
    assert movie is None


def test_repository_can_retrieve_movies_by_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_year(2014)

    # Check that the query returned 1 movies.
    assert len(movies) == 1


def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_for_a_given_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_year(2019)
    assert len(movies) == 0


def test_repository_can_retrieve_genres(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()

    assert len(genres) == 14

    assert Genre("Action") in genres
    assert Genre("Adventure") in genres
    assert Genre("Animation") in genres



def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Prometheus'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'Fantastic Beasts and Where to Find Them'


def test_repository_can_get_movies_by_ranks(in_memory_repo):
    movies = in_memory_repo.get_movies_by_rank([2, 5])

    assert len(movies) == 2
    assert movies[
               0].title == 'Prometheus'
    assert movies[1].title == "Suicranke Squad"


def test_repository_does_not_retrieve_movie_for_non_existent_rank(in_memory_repo):
    movies = in_memory_repo.get_movies_by_rank([2, 12])

    assert len(movies) == 1
    assert movies[
               0].title == 'Prometheus'


def test_repository_returns_an_empty_list_for_non_existent_ranks(in_memory_repo):
    movies = in_memory_repo.get_movies_by_rank([0, 20])

    assert len(movies) == 0


def test_repository_returns_movie_ranks_for_existing_genre(in_memory_repo):
    movie_ranks = in_memory_repo.get_movie_ranks_for_genre('Action')

    assert movie_ranks == [1, 5, 6,9]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    movie_ranks = in_memory_repo.get_movie_ranks_for_genre('dajia')

    assert len(movie_ranks) == 0


def test_repository_returns_year_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(3)
    previous_year = in_memory_repo.get_year_of_previous_movie(movie)

    assert previous_year == 2014


def test_repository_returns_none_when_there_are_no_previous_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    previous_year = in_memory_repo.get_year_of_previous_movie(movie)

    assert previous_year is None


def test_repository_returns_year_of_next_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    next_year = in_memory_repo.get_year_of_next_movie(movie)

    assert next_year == 2016


def test_repository_returns_none_when_there_are_no_subsequent_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(6)
    next_year = in_memory_repo.get_year_of_next_movie(movie)

    assert next_year is None


def test_repository_can_add_a_genre(in_memory_repo):
    genre = Genre('zhanzheng')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('ydia530')
    movie = in_memory_repo.get_movie(2)
    review = make_review( "Nice!", movie, user, datetime.today())
    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    review = Review(movie, "Nice movie!", None,  datetime.today())

    with pytest.raises(RepositoryException): in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_an_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('ydia530')
    movie = in_memory_repo.get_movie(0)
    review = Review(movie, "Excellent!", user, datetime.today())

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the movie doesn't refer to the review.
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 3
