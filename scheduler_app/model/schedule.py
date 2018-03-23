from setting import db, ma


class InterviewSchedule (db.Model):
    id = db.Column (db.Integer, primary_key=True)
    day = db.Column (db.String (10), nullable=False)
    start_time = db.Column (db.String (5), nullable=False)
    end_time = db.Column (db.String (5), nullable=False)

    candidate_email = db.Column (db.String (120), unique=True, nullable=False)
    interviewers_emails = db.Column (db.String (420), nullable=False)


class InterviewScheduleSchema (ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('day', 'start_time', 'end_time', 'candidate_email', 'interviewers_emails')
