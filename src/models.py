
import os
import sys
import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MediaType(enum.Enum):
    image = "image"
    video = "video"

class Follower(db.Model):
    __tablename__ = 'follower'
    user_from_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)

    posts = db.relationship('Post', back_populates='user')
    comments = db.relationship('Comment', back_populates='author')
    followers = db.relationship('Follower', foreign_keys=[Follower.user_to_id], backref='followed')
    following = db.relationship('Follower', foreign_keys=[Follower.user_from_id], backref='follower')

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post')
    media = db.relationship('Media', back_populates='post')

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(500))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    author = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(MediaType))
    url = db.Column(db.String(250))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship('Post', back_populates='media')

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20))
    birth_year = db.Column(db.String(20))
    eye_color = db.Column(db.String(20))
    height = db.Column(db.String(20))

    favorites = db.relationship('Favorite', back_populates='character')

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    population = db.Column(db.String(50))

    favorites = db.relationship('Favorite', back_populates='planet')

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)

    user = db.relationship('User')
    character = db.relationship('Character', back_populates='favorites')
    planet = db.relationship('Planet', back_populates='favorites')
