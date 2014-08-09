from hostessapp import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Sister(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    is_crib = db.Column(db.Boolean, default=False)
    bump_group_id = db.Column(db.Integer, db.ForeignKey('bump_group.id'))
    bump_group = db.relationship("BumpGroup", backref="sisters")


    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False 
    def get_id(self):
        return unicode(self.id)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return str(self.username)

class BumpGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    pnms = db.relationship("BumpToPnm",backref="bump_group")
    
    def __init__(self, name):
            self.name = name

class BumpToPnm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bump_id = db.Column(db.Integer, db.ForeignKey('bump_group.id'), primary_key=True)
    pnm_id = db.Column(db.Integer, db.ForeignKey('pnm.id'), primary_key=True)

    night = db.Column(db.Integer)
    party = db.Column(db.Integer)

    pnm = db.relationship("Pnm", backref="bump_assoc")

    def __init__(self, night, party):
        self.night = night
        self.party = party

class Pnm(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    major = db.Column(db.String(100))
    hometown = db.Column(db.String(100))
    year = db.Column(db.Integer)
    interests = db.Column(db.String(500))
    comments = db.relationship("Comment")


    def __init__(self, name, major, hometown, year, interests):
        self.name = name
        self.major = major
        self.hometown = hometown
        self.year = year
        self.interests = interests

    def __repr__(self):
        return str(self.name)

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    sister = db.Column(db.Integer, db.ForeignKey('sister.id'))
    sister_name = db.Column(db.String(30))
    pnm = db.Column(db.Integer, db.ForeignKey('pnm.id'))
    night = db.Column(db.Integer)
    party = db.Column(db.Integer)


    hidden = db.Column(db.Boolean, default=False)
    text = db.Column(db.String(1000))
    # to talk to - not making comment
    sisters = db.Column(db.String(200))
    interests = db.Column(db.String(200))


    def __init__(self, comment, interests, sisters, pnm, sister_id, name, night, party):
        self.text = comment
        self.pnm = pnm
        self.sister = sister_id
        self.sisters = sisters
        self.sister_name = name
        self.interests = interests
        self.night = night
        self.party = party


class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    night = db.Column(db.Integer, default=0)

def setup():
    db.create_all()
