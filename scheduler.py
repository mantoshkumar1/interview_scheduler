from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import backref
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'scheduler_db.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    schedule = db.relationship('EmployeeSchedule', backref=backref("employee", cascade="all,delete"))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Employee %r>' % self.name


class EmployeeSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __init__(self, day, start_time, end_time, emp_id):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.emp_id = emp_id


class EmployeeScheduleSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('day', 'start_time', 'end_time', 'emp_id')


employee_schema = EmployeeScheduleSchema()
employees_schema = EmployeeScheduleSchema(many=True)

# generating SQLite database
with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return 'Application is up!'


@app.route("/emp_schedule", methods=['GET'])
# schedule detail of all employees
def get_emp_schedule():
    all_emp = EmployeeSchedule.query.all()
    result = employees_schema.dump(all_emp)
    return jsonify(result.data)


# endpoint to add an employee schedule
@app.route("/emp_schedule", methods=['POST'])
def add_emp_schedule():
    name = request.json['name']
    email = request.json['email']
    day = request.json['day']
    start_time = request.json['start_time']
    end_time = request.json['end_time']

    emp = Employee.query.filter_by(email=email).first()

    # if emp does not exist, then make one otherwise employee scheduler entry will not be made.
    if not emp:
        emp = Employee(name, email)
        db.session.add(emp)
        db.session.commit()

    emp_schedule = EmployeeSchedule.query.filter_by(
        day=day,
        start_time=start_time,
        end_time=end_time,
        emp_id=emp.id
    ).first()

    if not emp_schedule:
        emp_schedule = EmployeeSchedule(day, start_time, end_time, emp.id)
        db.session.add(emp_schedule)
        db.session.commit()

    return employee_schema.jsonify(emp_schedule)


if __name__ == '__main__':
    app.run(debug=True)
