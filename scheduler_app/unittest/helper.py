from flask import json


class Helper:
    def __init__ ( self, app ):
        self.app = app

    @staticmethod
    def populate_dict ( given_dict, key_str, val ):
        if val:
            given_dict[ key_str ] = val

    def create_schedule ( self, name, email, day, start_time, end_time ):
        schedule = dict ( )
        self.populate_dict ( schedule, "name", name )
        self.populate_dict ( schedule, "email", email )
        self.populate_dict ( schedule, "day", day )
        self.populate_dict ( schedule, "start_time", start_time )
        self.populate_dict ( schedule, "end_time", end_time )

        return schedule

    def add_candidate_schedule ( self, name, email, day, start_time, end_time ):
        candidate_schedule_dict = self.create_schedule (
            name=name,
            email=email,
            day=day,
            start_time=start_time,
            end_time=end_time
        )

        # https://stackoverflow.com/questions/28836893/how-to-send-requests-with-jsons-in-unit-tests?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        response = self.app.post ( '/candidate_schedule',
                                   data=json.dumps ( candidate_schedule_dict ),
                                   content_type='application/json',
                                   follow_redirects=True )

        return response

    def get_candidates_schedules ( self ):
        response = self.app.get ( '/candidate_schedule',
                                  content_type='application/json',
                                  follow_redirects=True
                                  )
        return response

    def add_candidate_schedule_with_given_dict ( self, candidate_schedule_dict ):
        response = self.app.post ( '/candidate_schedule',
                                   data=json.dumps ( candidate_schedule_dict ),
                                   content_type='application/json',
                                   follow_redirects=True )

        return response

    def add_interviewer_schedule ( self, name, email, day, start_time, end_time ):
        interviewer_schedule_dict = self.create_schedule (
            name=name,
            email=email,
            day=day,
            start_time=start_time,
            end_time=end_time
        )

        response = self.app.post ( '/emp_schedule',
                                   data=json.dumps ( interviewer_schedule_dict ),
                                   content_type='application/json',
                                   follow_redirects=True )

        return response

    def add_interviewer_schedule_with_given_dict ( self, candidate_schedule_dict ):
        response = self.app.post ( '/emp_schedule',
                                   data=json.dumps ( candidate_schedule_dict ),
                                   content_type='application/json',
                                   follow_redirects=True )

        return response

    def get_employees_schedules ( self ):
        response = self.app.get ( '/emp_schedule',
                                  content_type='application/json',
                                  follow_redirects=True
                                  )
        return response

    def schedule_interview ( self, candidate_interviewers_dict ):
        response = self.app.post ( '/schedule_interview',
                                   data=json.dumps ( candidate_interviewers_dict ),
                                   content_type='application/json',
                                   follow_redirects=True )

        return response
