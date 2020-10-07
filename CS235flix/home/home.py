from flask import Blueprint, render_template

import CS235flix.utilities.utilities as utilities

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        '/home.html',
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls()

    )
