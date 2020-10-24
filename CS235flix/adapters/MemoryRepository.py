import csv
import os
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from CS235flix.adapters.repository import AbstractRepository, RepositoryException
from CS235flix.domain.model import Movie, User, Genre, Review, Actor, ModelException, Director


class memoryRepository(AbstractRepository):
    # Movies ordered by movie title and year, not rank. rank is assumed unique.
    def __init__(self):
        self._movies = list()
        self._movie_index = dict()
        self._genres = list()
        self._users = list()
        self._review = list()
        self._actor = list()
        self._directors = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.user_name == username), None)

    def get_reviews(self):
        return self._review

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movie_index[movie.rank] = movie

    def add_genre(self, genre:Genre):
        if genre not in self._genres:
            self._genres.append(genre)

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
            movie = self._movie_index[self._movies[0].rank]

        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movie_index[self.get_number_of_movies()]
        return movie

    def get_year_of_previous_movie(self, movie: Movie):
        previous_year = None

        try:
            index = self.movie_index(movie)
            for stored_movie in reversed(self._movies[0:index]):
                if stored_movie.release_year < movie.release_year:
                    previous_year = stored_movie.release_year
                    break
        except ValueError:
            # No earlier movies, so return None.
            pass

        return previous_year

    def get_year_of_next_movie(self, movie: Movie):
        next_year = None

        try:
            index = self.movie_index(movie)
            for stored_movie in self._movies[index + 1:len(self._movies)]:
                if stored_movie.release_year > movie.release_year:
                    next_year = stored_movie.release_year
                    break
        except ValueError:
            # No subsequent movies, so return None.
            pass

        return next_year

    def get_movies_by_year(self, target_year) -> List[Movie]:
        if target_year < 1900:
            target_year = 1900
        target_movie = Movie(
            year=int(target_year),
            title="x",
        )
        matching_movies = list()

        try:
            index = self.movie_index(target_movie)
            for movie in self._movies[index:None]:
                if movie.release_year == target_year:
                    matching_movies.append(movie)
                else:
                    break
        except ValueError:
            # No movies for specified year. Simply return an empty list.
            pass

        return matching_movies

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].release_year == movie.release_year:
            return index
        raise ValueError

    def get_genres(self):
        return self._genres

    def get_movies_by_rank(self, rank_list):
        # Strip out any ranks in rank_list that don't represent movie ranks in the repository.
        existing_ranks = [rank for rank in rank_list if rank in self._movie_index]
        # Fetch the movies.
        movies = [self._movie_index[rank] for rank in existing_ranks]
        return movies

    def get_movie_ranks_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a genre with the name genre_name.
        genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)


        # Retrieve the ranks of movies associated with the genre.
        if genre is not None:
            movie_ranks = [movie.rank for movie in genre.genre_movies]
        else:
            # No genre with name genre_name, so return an empty list.
            movie_ranks = list()

        return movie_ranks

    def get_movies_by_actor(self, actor_name):
        # Linear search, to find the first occurrence of a actor with the name actor_name.
        actor = next((actor for actor in self._actor if actor_name == actor.actor_full_name), None)
        if actor is not None:
            movie_list = actor.movies
        else:
            movie_list = list()

        return movie_list

    def get_movies_by_director(self, director_name: str):
        # Linear search, to find the first occurrence of a actor with the name actor_name.
        director = next((director for director in self._directors if director_name == director.director_full_name),
                        None)

        if director is not None:
            movie_list = director.movies
        else:
            movie_list = list()

        return movie_list

    def get_movies_by_movie_title(self, movie_title: str):
        #linear search to find the movie_title that user want.
        movies = list()
        for movie in self._movies:
            if movie.title == movie_title:
                movies.append(movie)
        return movies



    @property
    def genres(self):
        return self._genres

    @property
    def actor(self):
        return self._actor

    @genres.setter
    def genres(self, genre):
        self._genres.append(genre)

    def add_review(self, review):
        if review.user is None or review.movie is None:
            raise RepositoryException
        self._review.append(review)

    @actor.setter
    def actor(self, value):
        self._actor.append(value)

    @property
    def directors(self):
        return self._directors

    @directors.setter
    def directors(self, value):
        self._directors.append(value)


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


def load_movies_and_genre(data_path: str, repo: memoryRepository):
    genres = dict()
    actors = dict()
    directors = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'Data1000MoviesWithImage')):
        movie_genre = data_row[2].split(",")
        movie_actor = data_row[5].split(",")
        movie_actor = map(lambda x:x.strip(), movie_actor)
        movie_genre = map(lambda x: x.strip(), movie_genre)
        director = data_row[4]

        # Create Movie object.
        movie = Movie(data_row[1], int(data_row[6]))

        movie.rank = int(data_row[0])
        movie.description = data_row[3]
        movie.metascore = data_row[11]
        movie.votes = int(data_row[9])
        movie.rating =  float(data_row[8])

        if director not in directors:
            directors[director] = list()
        directors[director].append(movie.rank)



        # Add the Movie to the repository.
        repo.add_movie(movie)

        if data_row[-1] and data_row[-1] != 'N/A':
            movie.poster = data_row[-1]

        for genre in movie_genre:
            if genre not in genres.keys():
                genres[genre] = list()
            genres[genre].append(movie.rank)

        for actor in movie_actor:
            if actor not in actors.keys():
                actors[actor] = list()
            actors[actor].append(movie.rank)

    for director_name in directors.keys():
        director = Director(director_name)
        for rank in directors[director_name]:
            movie = repo.get_movie(rank)
            director.movies = movie
            movie.director = director
        if director not in repo.directors:
            repo.directors = director

    for genre_name in genres.keys():
        genre = Genre(genre_name)
        for rank in genres[genre_name]:
            movie = repo.get_movie(rank)
            genre.genre_movies = movie
            movie.genres = genre
        if genre not in repo.genres:
            repo.genres = genre

    for actor_name in actors.keys():
        actor = Actor(actor_name)
        for rank in actors[actor_name]:
            movie = repo.get_movie(rank)
            actor.movies = movie
            movie.actors = actor
        if actor not in repo.actor:
            repo.actor = actor


def load_users(data_path: str, repo: memoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_reviews(data_path: str, repo: memoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        review = make_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
            time=data_row[4]
        )
        repo.add_review(review)


def make_review(review_text: str, movie: Movie, user: User, time):
    review = Review(movie, review_text, user, time)
    user.add_review(review)
    movie.add_review(review)

    return review


def populate(data_path: str, repo: memoryRepository):
    # Load Movies and genre into the repository.
    load_movies_and_genre(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load reviews into the repository.
    load_reviews(data_path, repo, users)
