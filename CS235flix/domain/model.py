from typing import List, Iterable


class ModelException(Exception):
    pass


class Actor:
    def __init__(self, Actor_full_name: str):
        if Actor_full_name == "" or type(Actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = Actor_full_name.strip()
        self.__colleagues: List[Actor] = list()

        self.__movies = list()

    @property
    def movies(self):
        return self.__movies

    @movies.setter
    def movies(self, movie):
        self.__movies.append(movie)

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        return other.__actor_full_name == self.__actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        if isinstance(colleague, Actor):
            self.__colleagues.append(colleague)
            colleague.__colleagues.append(self)

    def check_if_this_actor_worked_with(self, colleague):
        for actor in self.__colleagues:
            if actor == colleague:
                return True
        return False


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

        self.__movies = list()

    @property
    def movies(self):
        return self.__movies

    @movies.setter
    def movies(self, movie: 'Movie'):
        self.__movies.append(movie)

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        if not isinstance(other, Director):
            return False
        return other.__director_full_name == self.__director_full_name

    def __lt__(self, other):
        return self.__director_full_name < other.__director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)


class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

        self.__genre_movies: List[Movie] = list()

    @property
    def genre_movies(self) -> Iterable['Movie']:
        return self.__genre_movies

    @genre_movies.setter
    def genre_movies(self, value):
        self.__genre_movies.append(value)

    @property
    def number_of_genre_movies(self) -> int:
        return len(self.__genre_movies)

    def is_applied_to(self, movie: 'Movie') -> bool:
        return movie in self.__genre_movies

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return other.__genre_name == self.__genre_name

    def __lt__(self, other):
        return self.__genre_name < other.__genre_name

    def __hash__(self):
        return hash(self.__genre_name)

    def add_movie(self, movie):
        self.__genre_movies.append(movie)


class Movie:
    def __init__(self, title: str, year: int):
        if title == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title: str = title.strip()
        if year < 1900:
            self.__release_year = None
        else:
            if type(year) == int:
                self.__release_year: int = year
            else:
                self.__release_year: int = None

        self.__description = None
        self.__director = None
        self.__actors: List[Actor] = list()
        self.__genres: List[Genre] = list()
        self.__runtime_minutes = None
        self.__votes = None
        self.__revenue = 'N/A'
        self.__metascore = None
        self.__rank = None
        self.__poster = None
        self.__reviews: List[Review] = list()
        self.__rating = None



    @property
    def reviews(self) -> Iterable["Review"]:
        return self.__reviews

    @reviews.setter
    def reviews(self, r: 'Review'):
        self.__reviews.append(r)

    @property
    def poster(self) -> str:
        return self.__poster

    @poster.setter
    def poster(self, url):
        if type(url) is str:
            self.__poster = url

    @property
    def title(self) -> str:
        return self.__title

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, descrip: str):
        if type(descrip) == str:
            self.__description = descrip.strip()

    @property
    def director(self) -> Director:
        return self.__director

    @director.setter
    def director(self, d: Director):
        if type(d) == Director:
            self.__director = d

    @property
    def actors(self) -> Iterable[Actor]:
        return self.__actors

    @actors.setter
    def actors(self, actor: Actor):
        if type(actor) == Actor:
            self.__actors.append(actor)

    @property
    def genres(self) -> Iterable["Genre"]:
        return self.__genres

    @genres.setter
    def genres(self, genre):
        self.__genres.append(genre)

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @property
    def rank(self) -> int:
        return self.__rank

    @rank.setter
    def rank(self, ran):
        if type(ran) is int:
            self.__rank = ran

    @runtime_minutes.setter
    def runtime_minutes(self, time: int):
        if type(time) == int and time >= 0:
            self.__runtime_minutes = time
        else:
            raise ValueError

    @property
    def rating(self) -> float:
        return self.__rating

    @rating.setter
    def rating(self, rate):
        self.__rating = rate

    @property
    def votes(self) -> int:
        return self.__votes

    @votes.setter
    def votes(self, vote: int):
        if type(vote) == int and vote >= 0:
            self.__votes = vote

    @property
    def revenue(self):
        return self.__revenue

    @revenue.setter
    def revenue(self, revenue: float):
        if type(revenue) == float and revenue >= 0:
            self.__revenue = revenue

    @property
    def metascore(self) -> int:
        return self.__metascore

    @metascore.setter
    def metascore(self, score: int):
        if type(score) == int and 0 <= score <= 100:
            self.__metascore = score

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        if self.__title == other.title and self.__release_year == other.release_year:
            return True
        return False

    def __lt__(self, other):
        if type(other) == Movie:
            return self.__release_year < other.release_year

    def __hash__(self):
        return hash(self.__title + str(self.__release_year))

    def add_review(self, review: 'Review'):
        self.__reviews.append(review)

    def add_actor(self, actor: Actor):
        if type(actor) == Actor:
            self.__actors.append(actor)

    def remove_actor(self, actor: Actor):
        for a in self.__actors:
            if a == actor:
                self.__actors.remove(a)

    def add_genre(self, genre: Genre):
        if type(genre) == Genre:
            self.__genres.append(genre)

    def remove_genre(self, genre: Genre):
        for a in self.__genres:
            if a == genre:
                self.__genres.remove(a)

    # interface for user voting the movie.
    def votes_the_movie(self):
        self.__votes += 1


class Review:
    def __init__(self, movie: Movie, review_text: str, user: 'User', time):
        self.__timestamp = time
        if type(movie) == Movie:
            self.__movie = movie
        else:
            self.__movie = None
        if type(review_text) == str:
            self.__review_text = review_text.strip()
        else:
            self.__review_text = None
        self.__rating = None
        self.__user = user

    @property
    def movie(self):
        return self.__movie

    @property
    def user(self):
        return self.__user

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp


    def __repr__(self):
        return f'<{self.__movie} {self.__timestamp}>'

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return (
                other.__timestamp == self.__timestamp and
                other.__review_text == self.__review_text and
                other.__rating == self.__rating
        )



class User:
    def __init__(self, user_name: str, password: str):
        if type(user_name) == str:
            self.__user_name = user_name.lower().strip()
        else:
            self.__user_name = None
        if type(password) == str:
            self.__password = password
        else:
            self.__password = None
        self.__watched_movies: List[Movie] = list()
        self.__reviews: List[Review] = list()
        self.__time_spend_watching_movies_minutes: int = 0

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spend_watching_movies_minutes

    def __repr__(self):
        return f'<User {self.__user_name}>'

    def __eq__(self, other):
        return self.__user_name == other.__user_name

    def __lt__(self, other):
        return self.__user_name < other.__user_name

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, movie: Movie):
        if type(movie) == Movie:
            self.__watched_movies.append(movie)
            self.__time_spend_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: Review):
        if type(review) == Review:
            self.__reviews.append(review)


class WatchList:
    def __init__(self):
        self.__watch_list: List[Movie] = list()

    def add_movie(self, movie: Movie):
        if movie not in self.__watch_list:
            self.__watch_list.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self.__watch_list:
            self.__watch_list.remove(movie)

    def size(self):
        return len(self.__watch_list)

    def select_movie_to_watch(self, index: int):
        if index < self.size():
            return self.__watch_list[index]
        else:
            return None

    def first_movie_in_watchlist(self):
        if self.size() == 0:
            return None
        else:
            return self.__watch_list[0]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < self.size():
            movie = self.__watch_list[self.index]
            self.index += 1
            return movie
        else:
            raise StopIteration
