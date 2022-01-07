from flask import Flask
from config import db


class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(30), index=False, unique=False, nullable=False)
    city = db.Column(db.String(30), index=False, unique=False, nullable=False)
    age = db.Column(db.String(30), index=False, unique=False, nullable=False)
    profilepic = db.Column(db.String(30), index=False,
                           unique=False, nullable=False)

    def __init__(self, userid, name, city, age, profilepic):
        self.name = name
        self.userid = userid
        self.city = city
        self.age = age
        self.profilepic = profilepic

    def serialize(self):
        return {'userid': self.userid, 'name': self.name, 'city': self.city, 'age': self.age, 'profilepic': self.profilepic}

    def __repr__(self):
        return str(self.serialize())
