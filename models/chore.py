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
        self.priority = priority  # integer tracking what priority a chore is with respect
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


'''
not too sure about using python for back end but anyways.  There should be a master list of all of the different chore
objects a family has created in the family class and members of the family would have a shorter, more tailored list 
(top twenty or so chores in it) which would be generated every day-or so, considering things such time since last 
completion, priority, what time of day it is and what the weather is like (for indoor/outdoor), as well as personal 
(or private) chores that aren't shared with the family.  This sublist can be manually regenerated too if want. 

In the application, the user can look at their sublist (primarily ordered by priority but can be changed for any other
filter and such) and the total family chore list or their private chore list.  One of the main aspects though of this
app idea is the card deck format of chores, to kinda make it like a poker game and less... chores.  This means you, the
player can ask the dealer to deal you out 3 cards that are shuffled (but still based on priority) and can be
shuffled again and again for up to five-or so times.  This deck will be what they need to complete that day (or more so 
quest items, that if they complete they get a buff or extra gold or experience).  

This should be like a game.  There will be in-game currency, collectable items, a shop, quests, achievements,
experience, levels, health, and challenges.  
- the currency can be used to pay other people to do that chore for you or to shuffle the deck an extra time or to
  buy different cosmetic items for your avatar or to purchase health.  This currency can be gained by completing 
  quests/achievements/challenges/level-ups.  (i can also try to incorporate gambling for more money).
- I also have an idea to make a "parent" or admin user that all the money will go back to when other members spend 
  money.
- experience can be gained from doing more or less the same things as currency but if you are really good with chores
  never miss them, you can get a multiplier.  
- Health can be lost.  There will be a preset value of health such as 10 and for everyday a chore is over due, they lose
  one health for each chore.  If they lose all of their health, the admit is notified and the member will become
  bankrupt, then they will be revived with 5 HP.  
- Quest items would be completing all of the cards delt by the dealer.  
- Achievements would be things such as "having a x day streak" or "doing an outdoor task while it rains" which would
  lead to money and experience.
- Challenges could be competing with other members of the family.  Maybe there can be a monthly and daily leader
  board and if you stay at the top for x amount of days, you get exp and currency.  You can also do bets with family 
  members of who would do more chores that day (though that may incentivise being fast over actually completing it).  
'''

