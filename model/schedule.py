from setting import db, ma
from sqlalchemy.orm import backref


class InterviewSchedule(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    day = db.Column (db.String (10), nullable=False)
    start_time = db.Column (db.String (5), nullable=False)
    end_time = db.Column (db.String (5), nullable=False)

    candidate_email = db.Column (db.String (120), unique=True, nullable=False)
    interviewers_emails = db.Column (db.String (420), nullable=False)

    #candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)


    #allocated_interviewers_id = db.Column(db.Integer, \
    #                                      db.ForeignKey('allocatedInterviewers.id'),\
    #                                      nullable=False)

    # email id of allocated interviewers
    #allocated_interviewers = db.relationship(
    #    'AllocatedInterviewers',
    #    backref=backref ("interviewschedule", cascade="all,delete")
    #)
class InterviewScheduleSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('day', 'start_time', 'end_time', 'candidate_email', 'interviewers_emails')

"""
class AllocatedInterviewers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    interviewers_email = db.Column (
        db.String (420),
        db.ForeignKey('interviewschedule.id'),
        unique=True,
        nullable=False
    )

    #interviewer_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

    def __init__(self, interviewers_email):
        self.interviewers_email = interviewers_email


class AllocatedInterviewersSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('interviewer_email')
"""

