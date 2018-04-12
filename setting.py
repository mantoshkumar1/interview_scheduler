from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

app = Flask ( __name__ )
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False
app.config[ 'BASEDIR' ] = os.path.abspath ( os.path.dirname ( __file__ ) )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///' + os.path.join ( app.config[ 'BASEDIR' ], \
                                                                        'scheduler_db.sqlite' )

db = SQLAlchemy ( app )

# used for serialization
ma = Marshmallow ( app )
