from flask import Blueprint, request, render_template
from templatesandmoe.modules.users.models import User
from templatesandmoe import db

mainModule = Blueprint('main', __name__, url_prefix='/')

@mainModule.route('/', methods=['GET'])
def home():
    return render_template("main/home.html")