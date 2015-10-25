from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Load configuration options from config.py
app.config.from_object('config')

# Setup database
db = SQLAlchemy(app)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db.engine))

# Import modules
from templatesandmoe.modules.main.controllers import mainModule as mainModule
from templatesandmoe.modules.auth.controllers import authModule as authModule
from templatesandmoe.modules.admin.controllers import adminModule as adminModule
from templatesandmoe.modules.api.controllers import apiModule as apiModule

# Register modules
app.register_blueprint(mainModule)
app.register_blueprint(authModule)
app.register_blueprint(adminModule)
app.register_blueprint(apiModule)