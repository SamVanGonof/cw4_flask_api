from flask_restx import Namespace, Resource

from project.setup.api.parsers import pr_page
from project.setup.api.models import director
from project.container import director_service

api = Namespace('directors')


@api.route('/')
class DirectorsView(Resource):
    @api.expect(pr_page)
    @api.marshal_with(director, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all directors.
        """
        return director_service.get_all(**pr_page.parse_args())


@api.route('/<int:director_id>/')
class DirectorView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(director, as_list=True, code=200, description='OK')
    def get(self, director_id: int):
        """
        Get director by id.
        """
        return director_service.get_item(director_id)
