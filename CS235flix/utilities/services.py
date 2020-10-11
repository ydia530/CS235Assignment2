from typing import Iterable
import random

from CS235flix.adapters.repository import AbstractRepository
from CS235flix.domain.model import Movie
from CS235flix.movie_blueprint.services import actors_to_string


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.genre_name for genre in genres]

    return genre_names


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of movies.
        quantity = movie_count - 1

    # Pick distinct and random movies.
    random_ids = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_rank(random_ids)
    return movies_to_dict(movies)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'year': movie.release_year,
        'title': movie.title,
        'poster': movie.poster,
        'director': movie.director,
        'actor': actors_to_string(movie.actors)
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
