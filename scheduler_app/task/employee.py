import datetime
import time

from flask import request, jsonify
from flask_api import status
from werkzeug.exceptions import BadRequest

from scheduler_app.model.employee import Employee, EmployeeSchedule, EmployeeScheduleSchema
from setting import db
from util import verify_rpc_value, commit_into_db


class EmpLogic:
    def __init__ ( self ):
        self.employee_schema = EmployeeScheduleSchema ( )
        self.employees_schema = EmployeeScheduleSchema ( many=True )

    @staticmethod
    def verify_post_data ( ):
        """
        Verify POST RPC data. If data is not supposed format, it raises appropriate error.
        :return:
        """
        valid_input_format = {"name": "Test", "email": "test@test.com", \
                              "day": "Monday",
                              "start_time": "16:30",
                              "end_time": "17:30"
                              }

        warning_msg = "Please provide input in following json format: " + str ( valid_input_format )

        # check every field is present and end_time is greater than start_time
        try:
            request.json[ 'name' ]

            # verify email format is correct
            # I assume user will provide only valid email address
            request.json[ 'email' ]

            # verify entry is Mon-Friday only
            if request.json[ 'day' ] not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'):
                return status.HTTP_400_BAD_REQUEST, {"Error: ": "Day format is incorrect", 'Fix': warning_msg}

            # verifying whether time is in 24 hours format only
            time.strptime ( request.json[ 'start_time' ], '%H:%M' )
            time.strptime ( request.json[ 'end_time' ], '%H:%M' )

            # verifying end_time is greater than start_time
            time_a = datetime.datetime.strptime ( request.json[ 'start_time' ], "%H:%M" )
            time_b = datetime.datetime.strptime ( request.json[ 'end_time' ], "%H:%M" )
            if time_b <= time_a:
                return status.HTTP_400_BAD_REQUEST, {"Error: ": "end_time is less/equal than start_time",
                                                     'Fix': warning_msg}

            verify_rpc_value ( request.json )

        except KeyError:  # All the values are not present
            return status.HTTP_400_BAD_REQUEST, {"Error": "All mandatory fields are not provided", 'Fix': warning_msg}
        except ValueError:  # time format of start_time and end_time is not in 24 hours format
            return status.HTTP_400_BAD_REQUEST, {
                "Error": "Time format is/are not in 24 hours format or one of the values is not string",
                'Fix': warning_msg}
        except BadRequest:
            return status.HTTP_400_BAD_REQUEST, {"Error": "All mandatory fields are not provided", 'Fix': warning_msg}

        return status.HTTP_200_OK, {"Success": "all ok"}

    def add_emp_schedule ( self ):
        """
        If an employee does not exist in Employee db, then it creates an instance of employee into Employee db
        Then this function adds the schedule of the employee into EmployeeSchedule db.
        :return: Json reply and http status code
        """
        status_code, error_msg = self.verify_post_data ( )
        if status_code != status.HTTP_200_OK:
            return jsonify ( error_msg ), status_code

        name = request.json[ 'name' ]
        email = request.json[ 'email' ]
        day = request.json[ 'day' ]
        start_time = request.json[ 'start_time' ]
        end_time = request.json[ 'end_time' ]

        emp = Employee.query.filter_by ( email=email ).first ( )

        # if emp does not exist, then make one otherwise employee scheduler entry will not be made.
        if not emp:
            emp = Employee ( name, email )
            db.session.add ( emp )

            # committing into db
            commit_into_db ( )

        emp_schedule = EmployeeSchedule.query.filter_by (
            day=day,
            start_time=start_time,
            end_time=end_time,
            emp_id=emp.id
        ).first ( )

        if not emp_schedule:
            emp_schedule = EmployeeSchedule ( day, start_time, end_time, emp.id )
            db.session.add ( emp_schedule )

            # committing into db
            commit_into_db ( )

        return self.employee_schema.jsonify ( emp_schedule ), status.HTTP_200_OK

    def get_emp_schedule ( self ):
        """
        This function returns all the values stored in EmployeeSchedule db
        :return: Json reply and http status code
        """
        all_emp = EmployeeSchedule.query.all ( )
        result = self.employees_schema.dump ( all_emp )
        return jsonify ( {"employees_schedules": result.data} ), status.HTTP_200_OK
