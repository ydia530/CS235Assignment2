
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import CS235flix.adapters.repository as repo
import CS235flix.utilities.utilities as utilities
import CS235flix.movie_blueprint.services as services

from CS235flix.authentication.authentication import login_required

# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/movies_by_year', methods=['GET'])
def movies_by_year():
    # Read query parameters.
    target_year = request.args.get('year')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    # Fetch the first and last movies in the series.
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if target_year is None:
        # No year query parameter, so return movies from first year of the series.
        movie = repo.repo_instance.get_first_movie()
        target_year = movie.release_year
    else:
        # Convert target_year from string to year.
        target_year = int(target_year)

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    # Fetch movie(s) for the target year. This call also returns the previous and next years for movies immediately
    # before and after the target year.
    movies, previous_year, next_year = services.get_movies_by_year(target_year, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies) > 0:
        # There's at least one movie for the target year.
        if previous_year is not None:
            # There are movies on a previous year, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movies_bp.movies_by_year', year=previous_year)
            first_movie_url = url_for('movies_bp.movies_by_year', year=first_movie['year'])

        # There are movies on a subsequent year, so generate URLs for the 'next' and 'last' navigation buttons.
        if next_year is not None:
            next_movie_url = url_for('movies_bp.movies_by_year', year=next_year)
            last_movie_url = url_for('movies_bp.movies_by_year', year=last_movie['year'])

        # Construct urls for viewing movie reviews and adding reviews.
        for movie in movies:
            movie['view_review_url'] = url_for('movies_bp.movies_by_year', year=target_year,
                                               view_reviews_for=movie['rank'])
            movie['add_review_url'] = url_for('movies_bp.reviews_on_movie', movie=movie['rank'])

        # Generate the webpage to display the movies.
        return render_template(
            'movies/movies.html',
            title='movies',
            movies_title=target_year,
            movies=movies,
            selected_movies=utilities.get_selected_movies(len(movies) * 2),
            genre_urls=utilities.get_genres_and_urls(),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url,
            show_reviews_for_movie=movie_to_show_reviews
        )

    # No movies to show, so return the homepage.
    return redirect(url_for('home_bp.home'))


@movies_blueprint.route('/reviews', methods=['GET', 'POST'])
@login_required
def reviews_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an movie rank, when subsequently called with a HTTP POST request, the movie rank remains in the
    # form.
    form = reviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the reviews text has passed data validation.
        # Extract the movie rank, representing the review movie, from the form.
        movie_rank = int(form.movie_rank.data)

        # Use the service layer to store the movie reviews.
        services.add_reviews(movie_rank, form.review.data, username, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_rank, repo.repo_instance)

        # Cause the web browser to display the page of all movies that have the same year as the reviewed movie,
        # and display all reviews, including the movie reviews.
        return redirect(url_for('movies_bp.movies_by_year', year=movie['year'], view_reviews_for=movie_rank))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie rank, representing the movie to review, from a query parameter of the GET request.
        movie_rank = int(request.args.get('movie'))

        # Store the movie rank in the form.
        form.movie_rank.data = movie_rank
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the movie rank of the movie being reviewed from the form.
        movie_rank = int(form.movie_rank.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    movie = services.get_movie(movie_rank, repo.repo_instance)
    return render_template(
        'movies/reviews_on_movie.html',
        title='Edit review',
        movie=movie,
        form=form,
        handler_url=url_for('movies_bp.reviews_on_movie'),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls()
    )


@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    movies_per_page = 3

    # Read query parameters.
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie rank.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ranks for movie's genre with genre_name.
    movie_ranks = services.get_movie_ranks_for_genre(genre_name, repo.repo_instance)

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_rank(movie_ranks[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(movie_ranks):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ranks) / movies_per_page)
        if len(movie_ranks) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews.
    for movie in movies:
        movie['view_review_url'] = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor,
                                           view_reviews_for=movie['rank'])
        movie['add_review_url'] = url_for('movies_bp.reviews_on_movie', movie=movie['rank'])

    # Generate the webpage to display the movies.
    return render_template(
        'movies/movies.html',
        title='movies',
        movies_title=genre_name + " Movies",
        movies=movies,
        selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class reviewForm(FlaskForm):
    review = TextAreaField('review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    movie_rank = HiddenField("movie_rank")
    submit = SubmitField('Submit')
