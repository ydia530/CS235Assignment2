import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from CS235flix.adapters.repository import AbstractRepository, RepositoryException
from CS235flix.domain.model import Movie, User, Genre, Review


class MemoryRepository(AbstractRepository):
    # Movies ordered by movie title and year, not rank. rank is assumed unique.
    def __init__(self):
        self._movies = list()
        self._movie_index = dict()
        self._genres = list()
        self._users = list()
        self._review = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.user_name == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movie_index[movie.rank] = movie

    def get_movie(self, rank: int) -> Movie:
        movie = None
        try:
            movie = self._movie_index[rank]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_genres(self):
        return self._genres


    def get_movies_by_rank(self, rank_list):
        # Strip out any ranks in rank_list that don't represent movie ranks in the repository.
        existing_ranks = [rank for rank in rank_list if rank in self._movie_index]
        # Fetch the movies.
        movies = [self._movie_index[rank] for rank in existing_ranks]
        return movies

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, value):
        self._genres.append(value)


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies_and_genre(data_path: str, repo: MemoryRepository):
    for data_row in read_csv_file(os.path.join(data_path, 'Data1000MoviesWithImg.csv')):
        movie_genre = data_row[2].split(",")
        movie_actor = data_row[2].split(",")

        # Create Movie object.
        movie = Movie(data_row[1], int(data_row[6]))
        for g in movie_genre:
            gen =  Genre(g)
            movie.genres = gen
            if gen not in repo.genres:
                repo.genres = gen

        movie.genres = movie_genre
        movie.rank = int(data_row[0])
        if data_row[-1]:
            movie.poster = data_row[-1]

        # Add the Movie to the repository.
        repo.add_movie(movie)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def populate(data_path: str, repo: MemoryRepository):
    # Load Movies and genre into the repository.
    load_movies_and_genre(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)
