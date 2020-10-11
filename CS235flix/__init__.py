"""Initialize Flask app."""

import os

from flask import Flask

import CS235flix.adapters.repository as repo
from CS235flix.adapters.MemoryRepository import memoryRepository, populate


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = os.path.join('CS235flix', 'adapters', 'data')

    if test_config is not None:
        # Load test configuration, and overrranke any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = memoryRepository()
    populate(data_path, repo.repo_instance)

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .movie_blueprint import movies
        app.register_blueprint(movies.movies_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)


    return app
