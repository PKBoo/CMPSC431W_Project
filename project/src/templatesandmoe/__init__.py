from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

# Import modules
from templatesandmoe.modules.main.controllers import mainModule as mainModule

app = Flask(__name__)

# Load configuration options from config.py
app.config.from_object('config')

# Setup database
db = SQLAlchemy(app)

# Register modules
app.register_blueprint(mainModule)