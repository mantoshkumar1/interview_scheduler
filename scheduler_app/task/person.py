from flask import request, abort
from flask_api import status
import time, datetime, sqlite3
from werkzeug.exceptions import BadRequest
from sqlalchemy import exc

from setting import db


class Person:
    @staticmethod
    def verify_rpc_value ( user_dict ):
        for key in user_dict:
            if type ( user_dict[ key ] ) == unicode or type ( user_dict[ key ] ) == str:
                continue
            else:
                raise ValueError ( 'Value is not String' )

    @classmethod
    def verify_post_data ( cls ):
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

            cls.verify_rpc_value ( request.json )

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

    @classmethod
    def commit_into_db ( cls, content, add_operation = True ):
        """
        Safely commit the content into db
        :return:
        """
        if add_operation:
            db.session.add ( content )
        else:
            if content:
                db.session.delete ( content )

        try:
            db.session.commit ( )
        except AssertionError as err:
            db.session.rollback ( )
            abort ( status.HTTP_409_CONFLICT, err )
        except (
                exc.IntegrityError,
                sqlite3.IntegrityError
        ) as err:
            db.session.rollback ( )
            abort ( status.HTTP_409_CONFLICT, err.orig )
        except Exception as err:
            db.session.rollback ( )
            abort ( status.HTTP_500_INTERNAL_SERVER_ERROR, err )
        finally:
            pass
            # db.session.close ( )
