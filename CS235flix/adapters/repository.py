import abc
from typing import List

from CS235flix.domain.model import Movie, User, Genre

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    def __init__(self):
        self.years = None

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

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the genre stored in the repository. """

        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_year(self, target_year):
        """ Returns movies stored in the repository at target year. """

        raise NotImplementedError

    @abc.abstractmethod
    def get_year_of_previous_movie(self, param):
        """ Returns movies stored in the repository at previous year. """

        raise NotImplementedError

    @abc.abstractmethod
    def get_year_of_next_movie(self, param):
        """ Returns movies stored in the repository at next year. """

        raise NotImplementedError

    def add_review(self, review):
        """   add reviews   """

        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ranks_for_genre(self, genre_name: str):
        """
        Returns a list of ranks representing  movies that are genre by genre_name.
        If there are no Movies that are genreged by genre_name, this method returns an empty list.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, actor_name: str):
        """
        Returns a list of movie that are contain a specific actor.
        If there are no Movies there, this method returns an empty list.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, director_name: str):
        """
        Returns a list of movie that are contain a specific director.
        If there are no Movies there, this method returns an empty list.

        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_movie_title(self, movie_title: str):
        """
        Returns a list of movie that are contain a specific movie title.
        If there are no Movies there, this method returns an empty list.

        """
        raise NotImplementedError
