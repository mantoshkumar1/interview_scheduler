from flask_api import status

from scheduler_app.task.candidate import CandidateLogic
from scheduler_app.task.employee import EmpLogic
from scheduler_app.task.schedule_algo import ScheduleAlgo
from setting import app, db

emp_logic = EmpLogic ( )
candidate_logic = CandidateLogic ( )
schedule_logic = ScheduleAlgo ( )

# generating SQLite database
with app.app_context ( ):
    db.create_all ( )


@app.route ( '/' )
def hello_world ( ):
    return 'Application is up!'


# schedule detail of all employees
@app.route ( "/emp_schedule", methods=[ 'GET' ] )
def get_emp_schedule ( ):
    return emp_logic.get_emp_schedule ( )


# endpoint to add an employee schedule
@app.route ( "/emp_schedule", methods=[ 'POST' ] )
def add_emp_schedule ( ):
    return emp_logic.add_emp_schedule ( )


@app.route ( "/candidate_schedule", methods=[ 'GET' ] )
# schedule detail of all candidates
def get_candidate_schedule ( ):
    return candidate_logic.get_all_candidate_schedule ( )


# endpoint to add a candidate schedule
@app.route ( "/candidate_schedule", methods=[ 'POST' ] )
def add_candidate_schedule ( ):
    return candidate_logic.add_candidate_schedule ( )


# endpoint to find an interview schedule time of a candidate with list of interviewers
@app.route ( "/schedule_interview", methods=[ 'POST' ] )
def calculate_schedule_interview ( ):
    return schedule_logic.calculate_schedule_interview ( )


# endpoint to fetch an interview schedule time of a candidate with list of interviewers
@app.route ( "/schedule_interview", methods=[ 'GET' ] )
def get_schedule_interview ( ):
    return schedule_logic.get_schedule_interviews ( )


# endpoint to reset the dbs
@app.route ( "/reset_scheduler", methods=[ 'GET', 'POST' ] )
def reset_application ( ):
    return schedule_logic.reset_scheduler_dbs_for_next_week ( )


@app.errorhandler ( status.HTTP_409_CONFLICT )
def handle_client_request_conflict ( error ):
    return error, status.HTTP_409_CONFLICT


@app.errorhandler ( status.HTTP_500_INTERNAL_SERVER_ERROR )
def handle_server_internal_error ( error ):
    return error, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.errorhandler ( status.HTTP_404_NOT_FOUND )
def page_not_found ( error ):
    return "The page user has requested doesn't exist", status.HTTP_404_NOT_FOUND


if __name__ == '__main__':
    app.run ( debug=False )
