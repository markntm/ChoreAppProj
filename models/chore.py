from flask import Flask
from models import db
import enum
from datetime import datetime, UTC


class Difficulty(enum.Enum):
    Simple = 1
    Easy = 2
    Medium = 3
    Hard = 4


class Priority(enum.Enum):
    Low = 1
    Medium = 2
    High = 3
    Highest = 4


class FreqTime(enum.Enum):
    Daily = 1
    Weekly = 7
    Monthly = 30
    Biyearly = 182
    Yearly = 365


class Category(enum.Enum):
    Indoor = 1
    Outdoor = 2
    Misc = 3


class Status(enum.Enum):
    Not_Started = 1
    In_Progress = 2
    Paused = 3
    Completed = 4


class ChoreParent(db.Model):
    def __init__(self, name, family_id, description="", category=Category.Misc, difficulty=Difficulty.Simple,
                 priority=Priority.Low):
        self.name = name
        self.description = description
        self.category = category
        self.difficulty = difficulty
        self.priority = priority
        self.family_id = family_id


class ChoreItem(ChoreParent, db.Model):
    __tablename__ = 'chore_list'  # db table name

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    category = db.Column(db.Enum(Category), nullable=False)
    difficulty = db.Column(db.Enum(Difficulty))
    priority = db.Column(db.Enum(Priority))
    time_expected = db.Column(db.Integer, nullable=False)  # in minutes
    time_average = db.Column(db.Integer, nullable=False)  # in minutes
    frequency = db.Column(db.Integer, nullable=False)
    frequency_unit = db.Column(db.Enum(FreqTime))

    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)

    def __init__(self, name, family_id, description, category, difficulty, priority, time_expected=60, time_average=60,
                 frequency=1, frequency_unit=FreqTime.Daily):
        super().__init__(name, family_id, description, category, difficulty, priority)
        self.time_expected = time_expected
        self.time_average = time_average
        self.frequency = frequency
        self.frequency_unit = frequency_unit


class CompChore(ChoreParent, db.Model):
    __tablename__ = 'completed_chores'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    category = db.Column(db.Enum(Category), nullable=False)
    difficulty = db.Column(db.Enum(Difficulty))
    priority = db.Column(db.Enum(Priority))
    comp_status = db.Column(db.Enum(Status))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    comp_time = db.Column(db.Integer, nullable=False)  # in minutes

    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, family_id, description, category, difficulty, priority, user_id, comp_status=Status.Not_Started,
                 start_time=(lambda: datetime.now(UTC))):
        super().__init__(name, family_id, description, category, difficulty, priority)
        self.comp_status = comp_status
        self.start_time = start_time
        self.user_id = user_id






