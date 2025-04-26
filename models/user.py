from flask import Flask
from models import db
from models.chore import ChoreItem, CompChore
import enum
from datetime import datetime, UTC


class Family(db.Model):
    """will hold a 'master list' of chores made by the family as well as holds an admin and family members.
       Requires a login name and password saved by the family admin."""
    __tablename__ = 'families'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    users = db.relationship('User', backref='family')  # hold instances of users in family
    family_chores = db.relationship('Chore', backref='family')  # hold instances of chores in family

    def __init__(self, name, password):
        self.name = name
        self.password = password


class User(db.Model):
    """Requires a user and password as well as a family to be a part of to function properly.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    currency = db.relationship('Currency', backref='user')
    health = db.relationship('Health', backref='user')
    levels = db.relationship('Level', backref='user')

    personal_chores = db.relationship('PersonalChore', backref='user')
    # I want to make a sublist for a specified list of 20~ chores generated for each user (both family and personal)
    family_admin = db.Column(db.Boolean, nullable=False)  # true if bro made the family or was chosen to be admin.
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))  # hold user connection to a family

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def chore_accepted(self, chore_id):
        chore = ChoreItem.query.filter_by(id=chore_id).first()

        if chore.family_id != self.family_id:
            return False

        accepted_chore = CompChore(
            name=chore.name,
            description=chore.description,
            category=chore.category,
            difficulty=chore.difficulty,
            priority=chore.priority,
            family_id=chore.family_id,
            user_id=chore.user_id
        )

        db.session.add(accepted_chore)
        db.session.commit()
        return True
