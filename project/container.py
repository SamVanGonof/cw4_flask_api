from project.dao import GenresDAO, DirectorDAO, MovieDAO, UserDAO

from project.services import GenresService, DirectorsService, MoviesService, UserService, UserMovieService
from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
director_dao = DirectorDAO(db.session)
movie_dao = MovieDAO(db.session)
user_dao = UserDAO(db.session)

# Services
genre_service = GenresService(dao=genre_dao)
director_service = DirectorsService(dao=director_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UserService(dao=user_dao)
user_movie_service = UserMovieService(dao_user=user_dao, dao_movie=movie_dao)
