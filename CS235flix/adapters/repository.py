import abc
from typing import List

from CS235flix.domain.model import Movie, User, Genre, Review

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, rank: int) -> Movie:
        """ Returns movie with rank from the repository.

        If there is no movie with the given rank, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the number of Movies in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first Movie, ordered by movie title and year, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last Movie, ordered by movie title and year, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_rank(self, rank_list):
        """ Returns a list of Movies, whose ranks match those in rank_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError