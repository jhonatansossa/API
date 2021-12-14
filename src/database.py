from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

db = SQLAlchemy()


class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.Text() , nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.now())
    updated_at=db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks = db.relationship('Bookmark', backref="user")

    def __repr__(self) -> str:
        return 'User >>> {self.username}'


class Bookmark(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    body=db.Column(db.Text, nullable=True)
    url=db.Column(db.Text, nullable=False)
    short_url=db.Column(db.String(3), nullable=True)
    visits=db.Column(db.Integer, default=0)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at=db.Column(db.DateTime, default=datetime.now())
    updated_at=db.Column(db.DateTime, onupdate=datetime.now())

    def generate_short_characters(self):
        characters=string.digits+string.ascii_letters
        picked_chars=''.join(random.choices(characters, k=3))

        link=self.query.filter_by(short_url=picked_chars).first()

        if link:
            self.generate_short_characters()
        else:
            return picked_chars


    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.short_url=self.generate_short_characters()

    def __repr__(self) -> str:
        return 'Bookmark >>> {self.url}'


class Relations(db.Model):
    ID=db.Column(db.String(2), primary_key=True)
    ACTIVEIMPORTID=db.Column(db.String(2), nullable=True)
    ACTIVEEXPORTID=db.Column(db.String(2), nullable=True)
    REACTIVEIMPORTID=db.Column(db.String(2), nullable=True)
    REACTIVEEXPORTID=db.Column(db.String(2), nullable=True)
    APPARENTIMPORTID=db.Column(db.String(2), nullable=True)
    APPARENTEXPORTID=db.Column(db.String(2), nullable=True)

    def __repr__(self) -> str:
        return 'Id >>> {self.ID}'


class Names(db.Model):
    ID=db.Column(db.String(2), primary_key=True)
    NAME=db.Column(db.String(30), nullable=True)

    def __repr__(self) -> str:
        return 'Name >>> {self.NAME}'

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'Id'         : self.ID,
           'Name': self.NAME
       }






