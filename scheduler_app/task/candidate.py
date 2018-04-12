import datetime
import time

from flask import request, jsonify
from flask_api import status
from werkzeug.exceptions import BadRequest

from scheduler_app.model.candidate import Candidate, CandidateSchedule, CandidateScheduleSchema
from setting import db
from util import verify_rpc_value, commit_into_db


class CandidateLogic:
    def __init__ ( self ):
        self.candidate_schema = CandidateScheduleSchema ( )
        self.candidates_schema = CandidateScheduleSchema ( many=True )

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

        warning_msg = 'Please provide input in following json format: ' + str ( valid_input_format )

        # check every field is present and end_time is greater than start_time
        try:
            request.json[ 'name' ]

            # verify email format is correct
            # I assume user will provide only valid email address
            request.json[ 'email' ]

            # verify entry is Mon-Friday only
            if request.json[ 'day' ] not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'):
                return status.HTTP_400_BAD_REQUEST, {"Error: ": "Day format is incorrect", 'Fix': warning_msg}

            # verifying whether time is in 24 hours format only otherwise raises ValueError
            time.strptime ( request.json[ 'start_time' ], '%H:%M' )
            time.strptime ( request.json[ 'end_time' ], '%H:%M' )

            # verifying end_time is greater than start_time
            time_a = datetime.datetime.strptime ( request.json[ 'start_time' ], "%H:%M" )
            time_b = datetime.datetime.strptime ( request.json[ 'end_time' ], "%H:%M" )

            if time_b <= time_a:
                return status.HTTP_400_BAD_REQUEST, {"Error: ": "end_time is less/equal than start_time",
                                                     'Fix': warning_msg}
                # return False, {"Error: ": "end_time is less/equal than start_time", 'Fix': warning_msg}

            verify_rpc_value ( request.json )

        except KeyError:  # All the values are not present (400 Bad Request)
            return status.HTTP_400_BAD_REQUEST, {"Error": "All mandatory fields are not provided", 'Fix': warning_msg}
        except ValueError:  # time format of start_time and end_time is not in 24 hours format
            return status.HTTP_400_BAD_REQUEST, {
                "Error": "Time format is/are not in 24 hours format or one of the values is not string",
                'Fix': warning_msg}
        except BadRequest:  # if request is not in json format
            return status.HTTP_400_BAD_REQUEST, {"Error": "All mandatory fields are not provided in json format",
                                                 'Fix': warning_msg}

        return status.HTTP_200_OK, {"Success": "all ok"}

    def add_candidate_schedule ( self ):
        """
        If candidate does not exist in Candidate db, then it creates an instance of candidate into Candidate db
        Then this function adds the schedule of the candidate into CandidateSchedule db.
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

        candidate = Candidate.query.filter_by ( email=email ).first ( )

        # if candidate does not exist, then make one otherwise candidate scheduler entry will not be made.
        if not candidate:
            candidate = Candidate ( name, email )
            db.session.add ( candidate )

            # committing into db
            commit_into_db ( )

        candidate_schedule = CandidateSchedule.query.filter_by (
            day=day,
            start_time=start_time,
            end_time=end_time,
            candidate_id=candidate.id
        ).first ( )

        if not candidate_schedule:
            candidate_schedule = CandidateSchedule ( day, start_time, end_time, candidate.id )
            db.session.add ( candidate_schedule )

            # committing into db
            commit_into_db ( )

        return self.candidate_schema.jsonify ( candidate_schedule ), status.HTTP_200_OK

    def get_all_candidate_schedule ( self ):
        """
        This function returns all the values stored in CandidateSchedule db
        :return: Json reply and http status code
        """
        all_candidate = CandidateSchedule.query.all ( )
        result = self.candidates_schema.dump ( all_candidate )
        return jsonify ( {"candidates_schedules": result.data} ), status.HTTP_200_OK
