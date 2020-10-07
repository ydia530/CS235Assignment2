import csv

from CS235flix.domain.model import Movie, Actor, Genre, Director


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.dataset_of_movies = []
        self.dataset_of_actors = []
        self.dataset_of_directors = []
        self.dataset_of_genres = []

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            index = 0
            for row in movie_file_reader:
                movie = Movie(row["Title"], int(row["Year"]))
                if movie not in self.dataset_of_movies:
                    self.dataset_of_movies.append(movie)

                for a in row["Actors"].split(","):
                    actor = Actor(a)
                    if actor not in self.dataset_of_actors:
                        self.dataset_of_actors.append(actor)
                director = Director(row["Director"])
                if director not in self.dataset_of_directors:
                    self.dataset_of_directors.append(director)

                for a in row["Genre"].split(","):
                    genre = Genre(a)
                    if genre not in self.dataset_of_genres:
                        self.dataset_of_genres.append(genre)
                index += 1


filename = '/Users/diaoyuan/Desktop/235/CS235FlixSkeleton/datafiles/Data1000Movies.csv'
movie_file_reader = MovieFileCSVReader(filename)
movie_file_reader.read_csv_file()

print(f'number of unique movies: {len(movie_file_reader.dataset_of_movies)}')
print(f'number of unique actors: {len(movie_file_reader.dataset_of_actors)}')
print(f'number of unique directors: {len(movie_file_reader.dataset_of_directors)}')
print(f'number of unique genres: {len(movie_file_reader.dataset_of_genres)}')
