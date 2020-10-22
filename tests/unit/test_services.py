import pytest

from CS235flix.authentication.services import AuthenticationException
from CS235flix.movie_blueprint import services as movie_services
from CS235flix.authentication import services as auth_services
from CS235flix.movie_blueprint.services import NonExistentmovieException


def test_can_add_user(in_memory_repo):
    new_username = 'abc'
    new_password = 'Q123'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'ydia530'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valrank_credentials(in_memory_repo):
    new_username = 'abcd'
    new_password = '1234567'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'abcd'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '1234', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_rank = 3
    review_text = 'I love this movie very much oh!'
    username = 'ydia530'

    # Call the service layer to add the review.
    movie_services.add_reviews(movie_rank, review_text, username, in_memory_repo)

    # Retrieve the reviews for the movie from the repository.
    movies_as_dict = movie_services.get_reviews_for_movie(movie_rank, in_memory_repo)

    # Check that the reviews include a review with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in movies_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_rank = 20
    review_text = "nice movie, enjoy!"
    username = 'ydia530'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movie_services.NonExistentmovieException):
        movie_services.add_reviews(movie_rank, review_text, username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_rank = 3
    review_text = 'I cant believe it!'
    username = 'gmichael'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movie_services.UnknownUserException):
        movie_services.add_reviews(movie_rank, review_text, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_rank = 2

    movie_as_dict = movie_services.get_movie(movie_rank, in_memory_repo)

    assert movie_as_dict['rank'] == movie_rank
    assert movie_as_dict['year'] == 2012
    assert movie_as_dict['title'] == 'Prometheus'
    assert movie_as_dict['description'] == "Following clues to the origin of mankind, a team finds a structure on a distant moon, but they soon realize they are not alone."
    assert movie_as_dict['poster'] == 'https://m.media-amazon.com/images/M/MV5BMTY3NzIyNTA2NV5BMl5BanBnXkFtZTcwNzE2NjI4Nw@@._V1_SX300.jpg'
    assert len(movie_as_dict['review']) == 0

    review_names = [dictionary['name'] for dictionary in movie_as_dict['genre']]
    assert 'Sci-Fi' in review_names
    assert 'Mystery' in review_names
    assert 'Adventure' in review_names


def test_cannot_get_movie_with_non_existent_rank(in_memory_repo):
    movie_rank = 100

    # Call the service layer to attempt to retrieve the Movie.
    with pytest.raises(movie_services.NonExistentmovieException):
        movie_services.get_movie(movie_rank, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movie_services.get_first_movie(in_memory_repo)
    print(movie_as_dict["title"])

    assert movie_as_dict['rank'] == 2


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movie_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['rank'] == 11


def test_get_movies_by_year_with_one_year(in_memory_repo):
    target_year = 2012

    movies_as_dict, prev_year, next_year = movie_services.get_movies_by_year(target_year, in_memory_repo)

    assert len(movies_as_dict) == 1
    assert movies_as_dict[0]['rank'] == 2

    assert prev_year is None
    assert next_year == 2014


def test_get_movies_by_year_with_multiple_years(in_memory_repo):
    target_year = 2014

    movies_as_dict, prev_year, next_year = movie_services.get_movies_by_year(target_year, in_memory_repo)

    # Check that there are 1 movies at 2012.
    assert len(movies_as_dict) == 1

    # Check that the movie ranks for the the movies returned are 3, 4 and 5.
    movie_ranks = [movie['rank'] for movie in movies_as_dict]
    assert {1}.issubset(movie_ranks)

    # Check that the years of movies surrounding the target_year are 2020-02-29 and 2020-03-05.
    assert prev_year == 2012
    assert next_year == 2016


def test_get_movies_by_year_with_non_existent_year(in_memory_repo):
    target_year = 2020

    movies_as_dict, prev_year, next_year = movie_services.get_movies_by_year(target_year, in_memory_repo)

    # Check that there are no movies year 2020.
    assert len(movies_as_dict) == 0


def test_get_movies_by_rank(in_memory_repo):
    target_movie_ranks = [1,2,20]
    movies_as_dict = movie_services.get_movies_by_rank(target_movie_ranks, in_memory_repo)

    # Check that 2 movies were returned from the query.
    assert len(movies_as_dict) == 2

    # Check that the movie ranks returned were 5 and 6.
    movie_ranks = [movie['rank'] for movie in movies_as_dict]
    assert {2, 1}.issubset(movie_ranks)


def test_get_reviews_for_movie(in_memory_repo):
    reviews_as_dict = movie_services.get_reviews_for_movie(1, in_memory_repo)

    # Check that 3 reviews were returned for movie with rank 1.
    assert len(reviews_as_dict) == 3

    # Check that the reviews relate to the movie whose rank is 1.
    movie_ranks = [review['movie_rank'] for review in reviews_as_dict]
    movie_ranks = set(movie_ranks)
    assert 1 in movie_ranks
    assert len(movie_ranks) == 1


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentmovieException):
        reviews_as_dict = movie_services.get_reviews_for_movie(20, in_memory_repo)


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    reviews_as_dict = movie_services.get_reviews_for_movie(2, in_memory_repo)
    assert len(reviews_as_dict) == 0



