from flask import request, jsonify
from model.candidate import Candidate, CandidateSchedule, CandidateScheduleSchema
from model.employee import Employee, EmployeeSchedule, EmployeeScheduleSchema
import datetime
from collections import defaultdict

class ScheduleAlgo:
    def __init__ (self):
        pass
        # todo: if write nothing, just delete this function.
        #self.candidates_schema = CandidateScheduleSchema (many=True)


    @staticmethod
    def get_interviewers_email():
        """
        This function retrieves the list of emails from the rest rpc which are separated by commas
        :return: List of interviewers email ids (str)
        """
        interviewers_email = request.json['interviewers_email']
        interviewers_email = interviewers_email.strip().split(', ')
        return interviewers_email

    def find_overlapping_time(self, t1, t2):
        """
        This functions finds overlapping time between two times, if overlapping
        time is not possible, it returns None, None.
        :param t1: (start_time, end_time)
        :param t2: (start_time, end_time)
        :return: (start_time, end_time)
        """
        # t1 = (11:00, 12:00), t2 = (11:30, 12:30) => (11:30, 12:00)
        # t1 = (11:30, 12:30), t2 = (11:00, 12:00) => (11:30, 12:00)
        # t1 = (11:00, 12:00), t2 = (14:30, 16:30) => (14:30, 12:00) Wrong
        start_time = max(t1[0], t2[0])
        end_time = min(t1[1], t2[1])

        if start_time >= end_time: return None, None

        return start_time, end_time


    def find_common_schedule_time(self, schedule_1, schedule_2):
        """
        This function finds the common schedule between two given schedules.
        If common schedule is not possible, it returns empty dictionary
        :param schedule_1: {day: [(start_time, end_time)]}
        :param schedule_2: {day: [(start_time, end_time)]}
        :return: {day: [(start_time, end_time)]}
        """
        common_schedule  = defaultdict(lambda:[])
        for day in schedule_1:
            times_1 = schedule_1[day]
            times_2 = schedule_2.get(day)
            if times_2 is None: continue

            for t1 in times_1:
                for t2 in times_2:
                    o_start_time, o_end_time  = self.find_overlapping_time(t1, t2)
                    if o_start_time is not None and\
                            (o_start_time, o_end_time) not in common_schedule[day]:
                        common_schedule[day].append((o_start_time, o_end_time))

        return common_schedule


    def calculate_schedule_interview (self):
        """
        This function fetches candidate and interviewers email ids and
        todo: write description later on.
        :return:
        """
        candidate_email = request.json['candidate_email']
        interviewers_email = self.get_interviewers_email()

        # fetching candidate schedule
        candidate = Candidate.query.filter_by (email=candidate_email).first ( )
        if not candidate:
            # todo: write code
            pass

        # todo: check if this candidate is already schedule or not
        # if he is already scheduled then no more processing and just return the result


        candidate_schedules = CandidateSchedule.query.filter_by (
            candidate_id=candidate.id
        ).all ( )

        fetched_candidate_schedules = defaultdict(lambda:[]) # {day: [(start_time, end_time)]}

        for c_schedule in candidate_schedules:
            day = c_schedule.day
            start_time = datetime.datetime.strptime (c_schedule.start_time, "%H:%M")
            end_time = datetime.datetime.strptime (c_schedule.end_time, "%H:%M")
            fetched_candidate_schedules[day].append((start_time, end_time))

        # fetching schedule of each interviewer
        for i_email in interviewers_email:
            interviewer = Employee.query.filter_by(email=i_email).first()

            # todo: check if interview exist, if not then just exit


            interviewer_schedules = EmployeeSchedule.query.filter_by (
                emp_id=interviewer.id
            ).all ( )

            fetched_interviewer_schedules = defaultdict (lambda: [])  # {day: [(start_time, end_time)]}
            for i_schedule in interviewer_schedules:
                day = i_schedule.day
                start_time = datetime.datetime.strptime (i_schedule.start_time, "%H:%M")
                end_time = datetime.datetime.strptime (i_schedule.end_time, "%H:%M")
                fetched_interviewer_schedules[day].append((start_time, end_time))

            # finding common time for each day between this interviewer and candidate
            # and store that result in fetched_candidate_schedules
            fetched_candidate_schedules = self.find_common_schedule_time(
                fetched_candidate_schedules,
                fetched_interviewer_schedules
            )

            # If candidate schedule becomes empty, means no scheduling possible anymore.
            # Therefore no point in doing more processing with other interviewers schedules.
            if not fetched_candidate_schedules:
                #todo: write code for this part later, return empty and do not save result in db
                pass

        # todo: now save the result in db
        # Now fetched_candidate_schedules has the common possible schedule
        # We choose a random entry from fetched_candidate_schedules dictionary
        fetched_candidate_schedules = fetched_candidate_schedules.items()
        import pdb;pdb.set_trace ( )

        if not fetched_candidate_schedules:
            # todo: write code for this part later, return empty and do not save result in db
            pass


        # [
        #   ( day, [ (start1, end1), (start2, end2) ] )
        # ]
        interview_day = fetched_candidate_schedules[0][0]
        interview_start_time = fetched_candidate_schedules[0][1][0][0]
        interview_end_time = fetched_candidate_schedules[0][1][0][1]


        # todo: create an instance of interview_day, start and end_time, candidate_email, interviewer emails
        # into the schedule db


        # todo: update interviewers schedules


        # todo: return these answers json through post rpc response


        return jsonify({"test":"test"})


    def get_schedule_interview (self):
        return jsonify ({"test":"test"})
