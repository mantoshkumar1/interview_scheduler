import unittest

from helper import Helper
# https://stackoverflow.com/questions/43307829/flask-returns-404-in-views?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
from run_scheduler import *


class BasicTests ( unittest.TestCase ):

    # executed prior to each test
    def setUp ( self ):
        app.config[ 'TESTING' ] = True
        app.config[ 'WTF_CSRF_ENABLED' ] = False
        app.config[ 'DEBUG' ] = False

        self.app = app.test_client ( )

        self.helper = Helper ( self.app )

    # executed after each test
    def tearDown ( self ):
        db.drop_all ( )
        db.create_all ( )

    #### tests ####

    def test_main_page ( self ):
        response = self.app.get ( '/', follow_redirects=True )
        self.assertEqual ( response.status_code, 200 )

    def test_invalid_page ( self ):
        response = self.app.get ( '/invalid_url', follow_redirects=True )
        self.assertEqual ( response.status_code, 404 )

    def test_fix_interview ( self ):
        """
        Integration test
        :return:
        """

        candidate_schedule = dict (
            name="Candidate 1",
            email="c1@gmail.com",
            day="Monday",
            start_time="14:00",
            end_time="15:00"
        )

        self.helper.add_candidate_schedule_with_given_dict ( candidate_schedule )

        candidate_schedule = dict (
            name="Candidate 1",
            email="c1@gmail.com",
            day="Wednesday",
            start_time="14:00",
            end_time="15:00"
        )
        self.helper.add_candidate_schedule_with_given_dict ( candidate_schedule )

        interview1_dict = dict (
            name="Employee 1",
            email="e1@gmail.com",
            day="Monday",
            start_time="14:00",
            end_time="15:00"
        )
        self.helper.add_interviewer_schedule_with_given_dict ( interview1_dict )

        interview1_dict = dict (
            name="Employee 1",
            email="e1@gmail.com",
            day="Friday",
            start_time="14:00",
            end_time="15:00"
        )
        self.helper.add_interviewer_schedule_with_given_dict ( interview1_dict )

        interview2_dict = dict (
            name="Employee 2",
            email="e2@gmail.com",
            day="Monday",
            start_time="14:00",
            end_time="16:00"
        )

        self.helper.add_interviewer_schedule_with_given_dict ( interview2_dict )

        interview2_dict = dict (
            name="Employee 2",
            email="e2@gmail.com",
            day="Tuesday",
            start_time="14:00",
            end_time="15:00"
        )

        self.helper.add_interviewer_schedule_with_given_dict ( interview2_dict )

        data = {
            "candidate_email": "c1@gmail.com",
            "interviewers_email": "e1@gmail.com, e2@gmail.com"
        }

        response = self.helper.schedule_interview ( data )
        self.assertEqual ( response.status_code, 200 )


if __name__ == "__main__":
    unittest.main ( )
