from flask import Blueprint, request, render_template

mainModule = Blueprint('main', __name__, url_prefix='/')


@mainModule.route('/', methods=['GET'])
def home():
    return render_template("main/home.html")