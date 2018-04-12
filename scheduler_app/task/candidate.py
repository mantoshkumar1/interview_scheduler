from flask import request, jsonify
from flask_api import status

from .person import Person
from ..model.candidate import Candidate, CandidateSchedule, CandidateScheduleSchema


class CandidateLogic ( Person ):
    def __init__ ( self ):
        self.candidate_schema = CandidateScheduleSchema ( )
        self.candidates_schema = CandidateScheduleSchema ( many=True )

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

            # committing into db
            self.commit_into_db ( candidate )

        candidate_schedule = CandidateSchedule.query.filter_by (
            day=day,
            start_time=start_time,
            end_time=end_time,
            candidate_id=candidate.id
        ).first ( )

        if not candidate_schedule:
            candidate_schedule = CandidateSchedule ( day, start_time, end_time, candidate.id )

            # committing into db
            self.commit_into_db ( candidate_schedule )

        return self.candidate_schema.jsonify ( candidate_schedule ), status.HTTP_200_OK

    def get_all_candidate_schedule ( self ):
        """
        This function returns all the values stored in CandidateSchedule db
        :return: Json reply and http status code
        """
        all_candidate = CandidateSchedule.query.all ( )
        result = self.candidates_schema.dump ( all_candidate )
        return jsonify ( {"candidates_schedules": result.data} ), status.HTTP_200_OK

    @staticmethod
    def fetch_candidate_obj_from_db ( candidate_email ):
        """
        This function fetches first candidate object from db matching candidate_email
        :param candidate_email: string
        :return: None or candidate object
        """
        candidate = Candidate.query.filter_by ( email=candidate_email ).first ( )
        return candidate

    def fetch_candidate_schedule_objs_from_db( self, candidate_id ):
        """
        This function fetches all the time slot choices objects saved in CandidateSchedule table
        :param candidate_id: int
        :return: None or candidate schedule objects
        """
        candidate_schedules = CandidateSchedule.query.filter_by ( candidate_id=candidate_id ).all ( )
        return candidate_schedules

    @staticmethod
    def reset_candidates_data ( ):
        """
        This function prepares CandidateSchedule and Candidate dbs for reset (notice no commit yet)
        :return:
        """
        from setting import db
        db.session.query ( CandidateSchedule ).delete ( )
        db.session.query ( Candidate ).delete ( )

