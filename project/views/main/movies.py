from flask_restx import Namespace, Resource

from project.container import movie_service
from project.setup.api import pr_movie, movie

api = Namespace('movies')


@api.route('/')
class MoviesView(Resource):
    @api.expect(pr_movie)
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all moves
        """
        return movie_service.get_all(**pr_movie.parse_args())


@api.route('/<int:movie_id>/')
class MovieView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(movie, code=200, description='OK')
    def get(self, movie_id: int):
        """
        Get movie by id.
        """
        return movie_service.get_item(movie_id)
