from flask import request, jsonify
from flask_api import status
from werkzeug.exceptions import BadRequest

import datetime
from collections import defaultdict

from ..model.schedule import InterviewSchedule, InterviewScheduleSchema

from .person import Person
from .candidate import CandidateLogic
from .employee import EmpLogic


class ScheduleAlgo ( Person ):
    def __init__ ( self ):
        self.emp_logic = EmpLogic ( )
        self.candidate_logic = CandidateLogic ( )
        self.interview_schema = InterviewScheduleSchema ( )
        self.interviews_schema = InterviewScheduleSchema ( many=True )

    @classmethod
    def verify_post_data ( cls ):
        """
        Overriding method defined in Person class.
        Verify POST RPC data. If data is not supposed format, it raises appropriate error.
        :return: status_code and collected data (error_msg or post_data)
        """
        valid_input_format = {
            "candidate_email": "candidate1@gmail.com",
            "interviewers_email": "interviewer1@gmail.com, interviewer2@gmail.com"
        }
        warning_msg = "Please provide input in following json format: " + str ( valid_input_format )

        # post rpc input verification and fetching
        try:
            candidate_email = request.json[ 'candidate_email' ]
            interviewers_email, interviewers_email_str = cls.get_interviewers_email ( )
            cls.verify_rpc_value ( request.json )
        except KeyError:
            return status.HTTP_400_BAD_REQUEST, {"Error": "All mandatory fields are not provided", 'Fix': warning_msg}
        except ValueError:
            return status.HTTP_400_BAD_REQUEST, {"Error": "One of the values is not string", 'Fix': warning_msg}
        except BadRequest:
            return status.HTTP_400_BAD_REQUEST, {"Error": "All mandatory fields are not provided in json format",
                                                 'Fix': warning_msg}

        return status.HTTP_200_OK, {"candidate_email": candidate_email, \
                                    "interviewers_email": interviewers_email, \
                                    "interviewers_email_str": interviewers_email_str}

    @staticmethod
    def get_interviewers_email ( ):
        """
        This function retrieves the list of emails collected from the rest rpc
        which are separated by commas.
        :return: set of unique interviewers email ids and a string containing their email ids
        """
        interviewers_email = request.json[ 'interviewers_email' ]

        interviewers_email = interviewers_email.replace ( ',', ' ' ).strip ( ).split ( )

        # verify same interviewer is not provided more than once
        # if any interviewer is requested more than once, we choose unique interviewers
        unique_interviewers = set ( )
        for i_email in interviewers_email:
            unique_interviewers.add ( i_email )

        return unique_interviewers, ", ".join ( unique_interviewers )

    @staticmethod
    def find_overlapping_time ( t1, t2 ):
        """
        This functions finds overlapping time between two times, if overlapping time is not possible, it returns None, None.

        Note: Both t1 and t2 contains a tuple of 2 elements, where each entry in those tuples are in datetime format.

        :param t1: (start_time, end_time)
        :param t2: (start_time, end_time)
        :return: (start_time, end_time)
        """
        # t1 = (11:00, 12:00), t2 = (11:30, 12:30) => (11:30, 12:00) Correct
        # t1 = (11:30, 12:30), t2 = (11:00, 12:00) => (11:30, 12:00) Correct
        # t1 = (11:00, 12:00), t2 = (14:30, 16:30) => (14:30, 12:00) Wrong
        start_time = max ( t1[ 0 ], t2[ 0 ] )
        end_time = min ( t1[ 1 ], t2[ 1 ] )

        if start_time >= end_time: return None, None

        return start_time, end_time

    @staticmethod
    def convert_datetime_to_str ( user_date_time ):
        """
        This function converts 24 hours datetime object to string
        :param user_date_time: datetime object in HH:MM format
        :return: string format of datetime in HH:MM format
        """
        return user_date_time.strftime ( "%H:%M" )

    @staticmethod
    def convert_str_to_datetime ( time_str ):
        """
        This function converts 24 hours string time to datetime object
        :param time_str:time in string (HH:MM format)
        :return: time in datetime object in HH:MM format
        """
        return datetime.datetime.strptime ( time_str, "%H:%M" )

    def find_common_schedule_time ( self, schedule_1, schedule_2 ):
        """
        This function finds the common schedule between two given schedules.
        If common schedule is not possible, it returns empty dictionary
        :param schedule_1: {day: [(start_time, end_time)]}
        :param schedule_2: {day: [(start_time, end_time)]}
        :return: {day: [(start_time, end_time)]}
        """
        common_schedule = defaultdict ( lambda: [ ] )
        for day in schedule_1:
            times_1 = schedule_1[ day ]
            times_2 = schedule_2.get ( day )
            if times_2 is None: continue

            for t1 in times_1:
                for t2 in times_2:
                    o_start_time, o_end_time = self.find_overlapping_time ( t1, t2 )
                    if o_start_time is not None and \
                            (o_start_time, o_end_time) not in common_schedule[ day ]:
                        common_schedule[ day ].append ( (o_start_time, o_end_time) )

        return common_schedule

    def calculate_schedule_interview ( self ):
        """
        This function fetches candidate and interviewers email ids and their corresponding availabilities.
        Based on their availabilities, it schedule an appointment with interviewers and candidate.
        If such appointment is successfully scheduled, then it removes the appointment time slot
        from interviewers availabilities and finally writes the appointment result in Schedule db.

        In case of any error, it provides the reason and fix of issue to the user.

        :return: Json reply and http status code
        """
        status_code, data = self.verify_post_data ( )
        if status_code != status.HTTP_200_OK:
            return jsonify ( data ), status_code

        candidate_email = data[ "candidate_email" ]
        interviewers_email = data[ "interviewers_email" ]
        interviewers_email_str = data[ "interviewers_email_str" ]

        # fetching first candidate object from db matching candidate_email
        candidate = self.candidate_logic.fetch_candidate_obj_from_db ( candidate_email )

        # checking if candidate exist, if not then just exit
        if not candidate:
            error_msg = "Candidate " + candidate_email + " does not exist"
            return jsonify (
                {"Error": error_msg, "Fix": "Create schedule entry for candidate first"} ), status.HTTP_403_FORBIDDEN

        # if candidate is already scheduled then no more processing and just return the result
        interview_schedule = InterviewSchedule.query.filter_by ( candidate_email=candidate_email ).first ( )
        if interview_schedule:  # interview is already scheduled
            return self.interview_schema.jsonify ( interview_schedule ), status.HTTP_200_OK

        # fetch time slot choices saved in CandidateSchedule table
        candidate_schedules = self.candidate_logic.fetch_candidate_schedule_objs_from_db ( candidate.id )

        common_schedule = defaultdict ( lambda: [ ] )  # {day: [(start_time, end_time)]}

        for c_schedule in candidate_schedules:
            day = c_schedule.day
            start_time = self.convert_str_to_datetime ( c_schedule.start_time )
            end_time = self.convert_str_to_datetime ( c_schedule.end_time )
            common_schedule[ day ].append ( (start_time, end_time) )

        # fetching schedule of each interviewer
        for i_email in interviewers_email:
            interviewer = self.emp_logic.fetch_emp_obj_from_db ( i_email )

            # checking if interviewer exist, if not then just exit
            if not interviewer:
                error_msg = "Interviewer " + i_email + " does not exist in company"
                return jsonify ( {"Error": error_msg, "Fix": "Hire that Guy first:)"} ), status.HTTP_403_FORBIDDEN

            interviewer_schedules = self.emp_logic.fetch_emp_schedule_objs_from_db ( interviewer.id )

            fetched_interviewer_schedules = defaultdict ( lambda: [ ] )  # {day: [(start_time, end_time)]}
            for i_schedule in interviewer_schedules:
                day = i_schedule.day
                start_time = self.convert_str_to_datetime ( i_schedule.start_time )
                end_time = self.convert_str_to_datetime ( i_schedule.end_time )
                fetched_interviewer_schedules[ day ].append ( (start_time, end_time) )

            # finding common time for each day between this interviewer and candidate
            # and store that result in common_schedule
            common_schedule = self.find_common_schedule_time (
                common_schedule,
                fetched_interviewer_schedules
            )

            # If candidate schedule becomes empty, means no scheduling possible anymore.
            # Therefore no point in doing more processing with other interviewers schedules.
            if not common_schedule:
                error_msg = "For next week, interview scheduling is not possible for " + candidate_email
                return jsonify (
                    {"Error": error_msg, "Fix": "Enter new availabilities for candidate"} ), status.HTTP_403_FORBIDDEN

        # Now common_schedule has the common possible schedule
        # We choose a random entry from common_schedule dictionary
        common_schedule = common_schedule.items ( )
        # [
        #   ( day, [ (start1, end1), (start2, end2) ] )
        # ]
        interview_day = common_schedule[ 0 ][ 0 ]
        interview_start_time = common_schedule[ 0 ][ 1 ][ 0 ][ 0 ]
        interview_end_time = common_schedule[ 0 ][ 1 ][ 0 ][ 1 ]

        # update interviewers schedules
        self.update_interviewers_timeslots ( interviewers_email,
                                             interview_day,
                                             interview_start_time, interview_end_time )

        # create an instance of schedule with interview_day, start and end_time, candidate_email, interviewer emails
        interview_schedule = self.prepare_interview_schedule_instance (
            interview_day,
            interview_start_time, interview_end_time,
            candidate_email,
            interviewers_email_str
        )

        # save the result in schedule db
        self.commit_into_db ( interview_schedule )

        # return json reply
        return self.interview_schema.jsonify ( interview_schedule ), status.HTTP_200_OK

    def prepare_interview_schedule_instance ( self, interview_day,
                                              interview_start_time, interview_end_time,
                                              candidate_email, interviewers_email ):
        """
        This function creates an instance of InterviewSchedule db and returns such.

        :param interview_day: day of the week in str format
        :param interview_start_time: 24 hours time in datetime format
        :param interview_end_time: 24 hours time in datetime format
        :param candidate_email: email of candidate in str format
        :param interviewers_email: emails of interviewers in str format
        :return: an instance of InterviewSchedule db
        """
        interview_schedule = InterviewSchedule (
            day=interview_day,
            start_time=self.convert_datetime_to_str ( interview_start_time ),
            end_time=self.convert_datetime_to_str ( interview_end_time ),
            candidate_email=candidate_email,
            interviewers_emails=interviewers_email
        )

        return interview_schedule

    def update_interviewers_timeslots ( self,
                                        interviewers_email,
                                        interview_day, interview_start_time, interview_end_time
                                        ):
        """
        Once an appointment is booked for a candidate, deleted the used time slot from interviewers
        available timeslots.

        :param interviewers_email: set of interviewer emails in str format
        :param interview_day: string format of the day in a week
        :param interview_start_time: datetime format in 24 hours
        :param interview_end_time: datetime format in 24 hours
        :return:
        """
        for i_email in interviewers_email:
            interviewer = self.emp_logic.fetch_emp_obj_from_db ( i_email )
            interviewer_schedules = self.emp_logic.fetch_emp_schedule_objs_from_db ( interviewer.id )

            for i_schedule in interviewer_schedules:
                day = i_schedule.day
                if day != interview_day: continue

                start_time = self.convert_str_to_datetime ( i_schedule.start_time )
                end_time = self.convert_str_to_datetime ( i_schedule.end_time )

                if start_time <= interview_start_time and interview_end_time <= end_time:
                    self.commit_into_db ( i_schedule, add_operation=False )
                    break

    def get_schedule_interviews ( self ):
        """
        This function returns this list of candidate and their scheduled appointment with interviewers
        :return: The calculated schedules of interviews for next week and http status code
        """
        all_schedule = InterviewSchedule.query.all ( )
        result = self.interviews_schema.dump ( all_schedule )
        return jsonify ( {"scheduled_interviews": result.data} ), status.HTTP_200_OK

    def reset_scheduler_dbs_for_next_week ( self ):
        """
        This function resets all the dbs and thus prepares the scheduler application for next week.
        :return: Json reply and http status code
        """

        # Note:  Order of execution matters for the sake of db integrity (Just to be holistic).
        # Don't worry, other order of below execution will not have impact on the application functionality.
        if request.method == 'GET':
            return "To reset dbs, send an empty post to the same URI"

        from setting import db
        db.session.query ( InterviewSchedule ).delete ( )

        self.emp_logic.reset_employees_data ( )
        self.candidate_logic.reset_candidates_data ( )

        self.commit_into_db ( content=None, add_operation=False )

        return jsonify ( {
            "Status": "Content of previous week is deleted from DBs. Application is now ready for use."} ), status.HTTP_200_OK
