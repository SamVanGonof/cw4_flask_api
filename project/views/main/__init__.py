from .genres import api as genres_ns
from .directors import api as director_ns
from .movies import api as movie_ns
from .users_movies import api as user_favorite_ns

__all__ = [
    'genres_ns',
    'director_ns',
    'movie_ns',
    'user_favorite_ns'
]
