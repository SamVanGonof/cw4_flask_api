from sqlalchemy import Column, String, TEXT, INT, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models, db


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)


movie_favorites = db.Table('movie_favorites',
                           models.Base.metadata,
                           Column('user_id', ForeignKey('users.id'), primary_key=True),
                           Column('movie_id', ForeignKey('movies.id'), primary_key=True))


class User(models.Base):
    __tablename__ = "users"

    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), unique=True, nullable=False)
    name = Column(String(20))
    surname = Column(String(20))
    favorite_genre_id = Column(INT(), ForeignKey('genres.id'))
    favorite_genre = relationship("Genre", foreign_keys=favorite_genre_id)
    movie_favorites = relationship("Movie", secondary=movie_favorites, back_populates='user_favorite')


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(100), unique=True, nullable=False)
    description = Column(TEXT(), nullable=False)
    trailer = Column(String(255), nullable=False)
    year = Column(INT(), nullable=False)
    rating = Column(Float(), nullable=False)
    genre_id = Column(INT(), ForeignKey("genres.id"))
    director_id = Column(INT(), ForeignKey("directors.id"))

    genre = relationship("Genre", foreign_keys=genre_id)
    director = relationship("Director", foreign_keys=director_id)
    user_favorite = relationship('User', secondary=movie_favorites, back_populates='movie_favorites')
