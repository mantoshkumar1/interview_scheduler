import unittest
from helper import Helper

# https://stackoverflow.com/questions/43307829/flask-returns-404-in-views?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
from run_scheduler import *


class BasicTests (unittest.TestCase):

    # executed prior to each test
    def setUp ( self ):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client ( )

        self.helper = Helper (self.app)

    # executed after each test
    def tearDown ( self ):
        db.drop_all ( )
        db.create_all ( )

    #### tests ####

    def test_main_page ( self ):
        response = self.app.get ('/', follow_redirects=True)
        self.assertEqual (response.status_code, 200)

    def test_add_valid_candidate_schedule ( self ):
        response = self.helper.add_candidate_schedule (
            name="Candidate 1",
            email="c1@gmail.com",
            day="Monday",
            start_time="14:00",
            end_time="15:00"
        )

        self.assertEqual (response.status_code, 200)

    def test_failed_candidate_schedule ( self ):
        data = [
            ("name", "Candidate 1"),
            ("email", "c1@gmail.com"),
            ("day", "Monday"),
            ("start_time", "13:00"),
            ("end_time", "14:00")
        ]

        for i in range (5):
            data_entry = data[i]
            data_used = {data_entry[0]: data_entry[1]}
            response = self.helper.add_candidate_schedule_with_given_dict (data_used)
            self.assertIn (b'Please provide input in following format', response.data)

    def test_empty_candidate_schedule ( self ):
        data = {}
        response = self.helper.add_candidate_schedule_with_given_dict (data)
        self.assertIn (b'Please provide input in following format', response.data)

    def test_add_valid_interviewer_schedule ( self ):
        response = self.helper.add_interviewer_schedule (
            name="Employee 1",
            email="e1@gmail.com",
            day="Monday",
            start_time="14:00",
            end_time="15:00"
        )

        self.assertEqual (response.status_code, 200)

    def test_failed_interviewer_schedule ( self ):
        data = [
            ("name", "Employee 1"),
            ("email", "e1@gmail.com"),
            ("day", "Monday"),
            ("start_time", "14:00"),
            ("end_time", "15:00")
        ]

        for i in range (5):
            data_entry = data[i]
            data_used = {data_entry[0]: data_entry[1]}
            response = self.helper.add_interviewer_schedule_with_given_dict (data_used)
            self.assertIn (b'Please provide input in following format', response.data)

    def test_empty_interviewer_schedule ( self ):
        data = {}
        response = self.helper.add_interviewer_schedule_with_given_dict (data)
        self.assertIn (b'Please provide input in following format', response.data)

    def test_fix_interview ( self ):

        candidate_schedule = dict (
            name="Candidate 1",
            email="c1@gmail.com",
            day="Monday",
            start_time="14:00",
            end_time="15:00"
        )

        self.helper.add_candidate_schedule_with_given_dict (candidate_schedule)

        candidate_schedule = dict (
            name="Candidate 1",
            email="c1@gmail.com",
            day="Wednesday",
            start_time="14:00",
            end_time="15:00"
        )
        self.helper.add_candidate_schedule_with_given_dict (candidate_schedule)

        interview1_dict = dict (
            name="Employee 1",
            email="e1@gmail.com",
            day="Monday",
            start_time="14:00",
            end_time="15:00"
        )
        self.helper.add_interviewer_schedule_with_given_dict (interview1_dict)

        interview1_dict = dict (
            name="Employee 1",
            email="e1@gmail.com",
            day="Friday",
            start_time="14:00",
            end_time="15:00"
        )
        self.helper.add_interviewer_schedule_with_given_dict (interview1_dict)

        interview2_dict = dict (
            name="Employee 2",
            email="e2@gmail.com",
            day="Monday",
            start_time="14:00",
            end_time="16:00"
        )

        self.helper.add_interviewer_schedule_with_given_dict (interview2_dict)

        interview2_dict = dict (
            name="Employee 2",
            email="e2@gmail.com",
            day="Tuesday",
            start_time="14:00",
            end_time="15:00"
        )

        self.helper.add_interviewer_schedule_with_given_dict (interview2_dict)

        self.test_add_valid_candidate_schedule ( )

        data = {
            "candidate_email": "c1@gmail.com",
            "interviewers_email": "e1@gmail.com"
        }

        response = self.helper.schedule_interview (data)

        self.assertEqual (response.status_code, 200)


if __name__ == "__main__":
    unittest.main ( )
