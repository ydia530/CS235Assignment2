from typing import List, Iterable

from CS235flix.adapters.repository import AbstractRepository
from CS235flix.domain.model import Movie, User, Genre, Review
from datetime import datetime


class NonExistentmovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def make_review(review_text, user, movie):
    review = Review(movie, review_text, user, datetime.today())
    user.add_review(review)
    movie.add_review(review)
    return review


def add_reviews(movie_rank: int, review_text: str, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(movie_rank)
    if movie is None:
        raise NonExistentmovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = make_review(review_text, user, movie)

    # Update the repository.
    repo.add_review(review)


def get_movie(rank: int, repo: AbstractRepository):
    movie = repo.get_movie(rank)

    if movie is None:
        raise NonExistentmovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_movies_by_year(year, repo: AbstractRepository):
    # Returns movies for the target year (empty if no matches), the year of the previous movie (might be null),
    # the year of the next movie (might be null)

    movies = repo.get_movies_by_year(target_year=year)
    m = repo.get_movies_by_year(2007)
    movies_dto = list()
    prev_year = next_year = None

    if len(movies) > 0:
        prev_year = repo.get_year_of_previous_movie(movies[0])
        next_year = repo.get_year_of_next_movie(movies[0])

        # Convert movies to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_year, next_year


def get_movie_ranks_for_genre(genre_name, repo: AbstractRepository):
    movie_ranks = repo.get_movie_ranks_for_genre(genre_name)

    return movie_ranks


def get_movies_by_rank(rank_list, repo: AbstractRepository):
    movies = repo.get_movies_by_rank(rank_list)

    # Convert movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_rank, repo: AbstractRepository):
    movie = repo.get_movie(movie_rank)

    if movie is None:
        raise NonExistentmovieException

    return reviews_to_dict(movie.reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'year': movie.release_year,
        'title': movie.title,
        'description': movie.description,
        'poster': movie.poster,
        'review': reviews_to_dict(movie.reviews),
        'genre': genres_to_dict(movie.genres),
        'director': movie.director.director_full_name,
        'actor': actors_to_string(movie.actors)
    }

    return movie_dict


def actors_to_string(actors):
    a = [actor.actor_full_name for actor in actors]
    return ", ".join(a)


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'username': review.user.user_name,
        'movie_rank': review.movie.rank,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'name': genre.genre_name,
        'genre_movies': [movie.rank for movie in genre.genre_movies]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dict):
    movie = Movie(dict.rank, dict.release_year, dict.title)
    # Note there's no reviews or genres.
    return movie
