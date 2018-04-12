from flask import request, jsonify
from flask_api import status

from .person import Person
from ..model.employee import Employee, EmployeeSchedule, EmployeeScheduleSchema


class EmpLogic ( Person ):
    def __init__ ( self ):
        self.employee_schema = EmployeeScheduleSchema ( )
        self.employees_schema = EmployeeScheduleSchema ( many=True )

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

            # committing into db
            self.commit_into_db ( emp )

        emp_schedule = EmployeeSchedule.query.filter_by (
            day=day,
            start_time=start_time,
            end_time=end_time,
            emp_id=emp.id
        ).first ( )

        if not emp_schedule:
            emp_schedule = EmployeeSchedule ( day, start_time, end_time, emp.id )

            # committing into db
            self.commit_into_db ( emp_schedule )

        return self.employee_schema.jsonify ( emp_schedule ), status.HTTP_200_OK

    def get_emp_schedule ( self ):
        """
        This function returns all the values stored in EmployeeSchedule db
        :return: Json reply and http status code
        """
        all_emp = EmployeeSchedule.query.all ( )
        result = self.employees_schema.dump ( all_emp )
        return jsonify ( {"employees_schedules": result.data} ), status.HTTP_200_OK

    @staticmethod
    def fetch_emp_obj_from_db ( interviewer_email ):
        """
        This function fetches first employee object from db matching interviewer_email
        :param interviewer_email: string
        :return: None or employee object
        """
        interviewer = Employee.query.filter_by ( email=interviewer_email ).first ( )
        return interviewer

    @staticmethod
    def fetch_emp_schedule_objs_from_db( emp_id ):
        """
        This function fetches all the time slot choices objects saved in EmployeeSchedule table
        :param emp_id: int
        :return: None or employee schedule objects
        """
        interviewer_schedules = EmployeeSchedule.query.filter_by (emp_id=emp_id).all ( )
        return interviewer_schedules

    @staticmethod
    def reset_employees_data(  ):
        """
        This function prepares EmployeeSchedule and Employee dbs for reset (notice no commit yet)
        :return:
        """
        from setting import db
        db.session.query ( EmployeeSchedule ).delete ( )
        db.session.query ( Employee ).delete ( )
