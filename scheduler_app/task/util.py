import sqlite3

from flask import abort
from flask_api import status
from sqlalchemy import exc

from setting import db


def verify_rpc_value ( user_dict ):
    for key in user_dict:
        if type ( user_dict[ key ] ) == unicode or type ( user_dict[ key ] ) == str:
            continue
        else:
            raise ValueError ( 'Value is not String' )


def commit_into_db ( ):
    """
    Safely commit the content into db
    :return:
    """
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
