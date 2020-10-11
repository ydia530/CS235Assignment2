from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import CS235flix.utilities.utilities as utilities
import CS235flix.search.services as services
import CS235flix.adapters.repository as repo

# Configure Blueprint.
search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    dosearch = None
    result = None
    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None
    search_content = request.args.get('content')
    if form.validate_on_submit():
        content = form.content.data
        return redirect(url_for('search_bp.search', content=content))

    if request.method == 'GET':
        dosearch = "yes"
        try:
            if search_content is not None:
                search_content = int(request.args.get('content'))
                result = repo.repo_instance.get_movies_by_year(search_content)
                result = services.movies_to_dict(result)

        except ValueError:
            result = services.get_movies_by_actor(search_content, repo.repo_instance)  # try search actor in repo
            if result is None:
                result = services.get_movies_by_director(search_content,
                                                         repo.repo_instance)  # try search director in repo
            if result is None:
                result = services.get_movies_by_movie_title(search_content,
                                                            repo.repo_instance)  # try search movie title in repo

        if result is not None and len(result) > 3:
            movies_per_page = 3
            cursor = request.args.get('cursor')
            if cursor is None:
                # No cursor query parameter, so initialise cursor to start at the beginning.
                cursor = 0
            else:
                # Convert cursor from string to int.
                cursor = int(cursor)


            if cursor > 0:
                # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
                prev_movie_url = url_for('search_bp.search',  content=search_content, cursor=cursor - movies_per_page)
                first_movie_url = url_for('search_bp.search', content=search_content,)

            if cursor + movies_per_page < len(result):

                # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
                next_movie_url = url_for('search_bp.search', content=search_content,cursor=cursor + movies_per_page)

                last_cursor = movies_per_page * int(len(result) / movies_per_page)
                if len(result) % movies_per_page == 0:
                    last_cursor -= movies_per_page
                last_movie_url = url_for('search_bp.search', content=search_content, cursor=last_cursor)

            result = result[cursor:cursor + movies_per_page]
            for movie in result:
                movie['view_review_url'] = url_for('search_bp.search', content=search_content,cursor=cursor,
                                                   view_reviews_for=movie['rank'])
                movie['add_review_url'] = url_for('movies_bp.reviews_on_movie', movie=movie['rank'])
        if result is not None and len(result) == 0:
            result = None



    return render_template(
        'search.html',
        form=form,
        handler_url=url_for('search_bp.search'),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls(),
        result=result,
        dosearch=dosearch,
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        content = search_content
    )


class SearchForm(FlaskForm):
    content = StringField("content", [DataRequired()])
    submit = SubmitField("search")
