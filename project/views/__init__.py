from .auth import auth_ns, user_ns
from .main import genres_ns, director_ns, movie_ns, user_favorite_ns

__all__ = [
    'auth_ns',
    'genres_ns',
    'user_ns',
    'director_ns',
    'movie_ns',
    'user_favorite_ns'
]
