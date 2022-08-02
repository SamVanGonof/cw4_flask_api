from flask_restx import fields, Model

from project.setup.api.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Директор', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Квентин Тарантино'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='300 спартанцев'),
    'description': fields.String(required=True, max_length=100, example='Описание фильма'),
    'trailer': fields.String(required=True, example='https://www.youtube.com/watch?v=W85oD8FEF78&ab_channel=OwlKitty'),
    'year': fields.Integer(required=True, max_length=5, example=2020),
    'rating': fields.Float(required=True, max_length=5, example=5.5),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director),
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, example='name@email.com'),
    'name': fields.String(example='Валера'),
    'surname': fields.String(example='Зуев'),
    'favorite_genre': fields.Nested(genre)
})
