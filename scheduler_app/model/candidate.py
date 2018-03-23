from setting import db, ma
from sqlalchemy.orm import backref


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    schedule = db.relationship('CandidateSchedule', backref=backref("candidate"))

    def __init__ (self, name, email):
        self.name = name
        self.email = email


class CandidateSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))

    def __init__ (self, day, start_time, end_time, candidate_id):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.candidate_id = candidate_id


class CandidateScheduleSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('day', 'start_time', 'end_time', 'candidate_id')
