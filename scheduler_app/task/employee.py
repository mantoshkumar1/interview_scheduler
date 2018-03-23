from flask import request, jsonify
import datetime
import time

from setting import db
from scheduler_app.model.employee import Employee, EmployeeSchedule, EmployeeScheduleSchema




class EmpLogic:
    def __init__ (self):
        self.employee_schema = EmployeeScheduleSchema()
        self.employees_schema = EmployeeScheduleSchema(many=True)

    @staticmethod
    def verify_post_data ():
        valid_input_format = {'name': 'Test',
                              'email': 'test@test.com',
                              'day': 'Monday',
                              'start_time': '16:30',
                              'end_time': '17:30'
                              }
        warning_msg = "Please provide input in following format: " + str (valid_input_format)

        # check every field is present and end_time is greater than start_time
        try:
            request.json['name']

            # verify email format is correct
            # I assume user will provide only valid email address
            request.json['email']

            # verify entry is Mon-Friday only
            if request.json['day'] not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'):
                return False, {"Error: ": "Day format is incorrect", 'Fix': warning_msg}

            # verifying whether time is in 24 hours format only
            time.strptime(request.json['start_time'], '%H:%M')
            time.strptime(request.json['end_time'], '%H:%M')

            # verifying end_time is greater than start_time
            time_a = datetime.datetime.strptime(request.json['start_time'], "%H:%M")
            time_b = datetime.datetime.strptime(request.json['end_time'], "%H:%M")
            if time_b <= time_a:
                return False, {"Error: ": "end_time is less/equal than start_time", 'Fix': warning_msg}

        except KeyError:  # All the values are not present
            return False, {"Error": "All mandatory fields are not provided", 'Fix': warning_msg}
        except ValueError:  # time format of start_time and end_time is not in 24 hours format
            return False, {"Error": "Time format is/are not in 24 hours format", 'Fix': warning_msg}

        return True, {"Success" : "all ok"}

    def add_emp_schedule (self):
        is_data_ok, error_msg = self.verify_post_data()
        if not is_data_ok:
            return jsonify(error_msg)

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

        return self.employee_schema.jsonify(emp_schedule)

    def get_emp_schedule (self):
        all_emp = EmployeeSchedule.query.all()
        result = self.employees_schema.dump(all_emp)
        return jsonify(result.data)



