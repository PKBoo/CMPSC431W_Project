from flask import Flask
from flask import render_template

# Import modules
from templatesandmoe.modules.main.controllers import mainModule as mainModule

app = Flask(__name__)
app.register_blueprint(mainModule)