from flask import Blueprint, flash, redirect, render_template, session
from templatesandmoe import db_session
from templatesandmoe.modules.auth.forms.login import LoginForm
from templatesandmoe.modules.users.service import UserService

authModule = Blueprint('auth', __name__)
user_service = UserService(database=db_session)


@authModule.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = user_service.authenticate(form.username.data, form.password.data)
        if user:
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['permission'] = user.permissions

            return redirect('/')
        else:
            flash(u'Invalid username or password', 'error')
            return render_template('auth/login.html', form=form)
    else:
        return render_template('auth/login.html', form=form)


@authModule.route('/logout', methods=['GET'])
def logout():
    if session['user_id']:
        session.clear()

        return redirect('/')