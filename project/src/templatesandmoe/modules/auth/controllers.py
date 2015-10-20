from flask import Blueprint, request, render_template
from templatesandmoe.modules.auth.forms.login import LoginForm
from templatesandmoe.modules.users.models import User
from templatesandmoe import db

authModule = Blueprint('auth', __name__, url_prefix='/login')

@authModule.route('/', methods=['GET'])
def login_page():
    form = LoginForm()
    return render_template("auth/login.html", form=form)