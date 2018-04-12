import unittest

from run_scheduler import *
from .helper import Helper


class CandidateTests ( unittest.TestCase ):

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
    def test_add_valid_candidate_schedule ( self ):
        response = self.helper.add_candidate_schedule (
            name="Candidate 1",
            email="c1@gmail.com",
            day="Monday",
            start_time="14:00",
            end_time="15:00"
        )

        self.assertEqual ( response.status_code, 200 )

    def test_not_24_hours_starttime_format ( self ):
        response = self.helper.add_candidate_schedule (
            name="Candidate 1",
            email="c1@gmail.com",
            day="Monday",
            start_time="2:00 PM",
            end_time="15:00"
        )

        self.assertEqual ( response.status_code, 400 )

    def test_not_24_hours_endtime_format ( self ):
        response = self.helper.add_candidate_schedule (
            name="Candidate 1",
            email="c1@gmail.com",
            day="Monday",
            start_time="12:00",
            end_time="5:00"
        )

        self.assertEqual ( response.status_code, 400 )

    def test_starttime_greater_than_endtime ( self ):
        response = self.helper.add_candidate_schedule (
            name="Candidate 1",
            email="c1@gmail.com",
            day="Monday",
            start_time="14:00",
            end_time="11:00"
        )

        self.assertEqual ( response.status_code, 400 )

    def test_not_json_data ( self ):
        # name is not in json format
        response = self.helper.add_candidate_schedule (
            name='Candidate 1',
            email="c1@gmail.com",
            day="Monday",
            start_time="12:00",
            end_time="5:00"
        )


        self.assertEqual ( response.status_code, 400 )

    def test_failed_candidate_schedule ( self ):
        data = [
            ("name", "Candidate 1"),
            ("email", "c1@gmail.com"),
            ("day", "Monday"),
            ("start_time", "13:00"),
            ("end_time", "14:00")
        ]

        for i in range ( 5 ):
            # for every iteration, only one field will be posted to application, thus expect bad request status code
            data_entry = data[ i ]
            data_used = {data_entry[ 0 ]: data_entry[ 1 ]}
            response = self.helper.add_candidate_schedule_with_given_dict ( data_used )
            self.assertEqual ( response.status_code, 400 )

    def test_empty_candidate_schedule ( self ):
        data = {}
        response = self.helper.add_candidate_schedule_with_given_dict ( data )
        self.assertEqual ( response.status_code, 400 )

    def test_get_all_candidate_schedule ( self ):
        response = self.helper.get_candidates_schedules ( )
        self.assertEqual ( response.status_code, 200 )
