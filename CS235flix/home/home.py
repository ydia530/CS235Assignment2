from flask import Blueprint, render_template, url_for
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import CS235flix.adapters.repository as repo
import CS235flix.utilities.utilities as utilities
from CS235flix.utilities import services

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        '/home.html',
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls()

    )
