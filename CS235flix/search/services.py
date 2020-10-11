from typing import List, Iterable

from CS235flix.adapters.repository import AbstractRepository
from CS235flix.domain.model import Movie
from CS235flix.movie_blueprint.services import reviews_to_dict, genres_to_dict, actors_to_string


class UnValidInput(Exception):
    pass


def is_year(n: object) -> bool:
    if type(n) is not int:
        raise UnValidInput
    else:
        return True


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def get_movies_by_actor(data, repo):
    movies = repo.get_movies_by_actor(data)
    if not movies:
        return None

    return movies_to_dict(movies)


def get_movies_by_director(data, repo):

    movies = repo.get_movies_by_director(data)
    if not movies:
        return None
    return movies_to_dict(movies)


def get_movies_by_movie_title(data, repo):
    movies = repo.get_movies_by_movie_title(data)
    if not movies:
        return None
    return movies_to_dict(movies)


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
