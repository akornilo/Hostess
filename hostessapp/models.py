from hostessapp import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Sister(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
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


class PNM(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	major = db.Column(db.String(100))
	hometown = db.Column(db.String(100))
	year = db.Column(db.Integer)
	interests = db.Column(db.String(500))
	pros = db.Column(db.String(500))
	cons = db.Column(db.String(500))
	comments = db.Column(db.String(1000))
	#recommended sisters via app
	# sisters = db.Column(db.String(1000))

	def __init__(self, name, major, hometown, year, interests):
		self.name = name
		self.major = major
		self.hometown = hometown
		self.year = year
		self.interests = interests

	def __repr__(self):
		return str(self.name)

def setup():
	db.create_all()
