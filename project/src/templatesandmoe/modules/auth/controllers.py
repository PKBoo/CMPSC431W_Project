from flask import Blueprint, flash, redirect, render_template, session
from templatesandmoe.modules.auth.forms.login import LoginForm
from templatesandmoe.modules.users.models import User

authModule = Blueprint('auth', __name__)


@authModule.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
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