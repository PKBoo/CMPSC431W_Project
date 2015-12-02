from flask import Blueprint, flash, redirect, render_template, request, session
from templatesandmoe import db_session
from templatesandmoe.modules.auth.forms.login import LoginForm
from templatesandmoe.modules.auth.forms.register import RegisterForm
from templatesandmoe.modules.users.service import UsersService

authModule = Blueprint('auth', __name__)
users_service = UsersService(database=db_session)


@authModule.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users_service.authenticate(form.username.data, form.password.data)
        if user:
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['permission'] = user.permissions

            if session.get('previous_page'):
                return redirect(session.get('previous_page'))
            else:
                return redirect('/')
        else:
            flash(u'Invalid username or password', 'error')
            return render_template('auth/login.html', form=form)
    else:
        session['previous_page'] = request.referrer
        return render_template('auth/login.html', form=form)


@authModule.route('/logout', methods=['GET'])
def logout():
    if session['user_id']:
        session.clear()

        return redirect('/')


@authModule.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id') is None:
        form = RegisterForm()
        if form.validate_on_submit():
            if not users_service.exists(form.username.data):
                new_user = users_service.create(
                    username=form.username.data,
                    password=form.password.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    permissions=0
                )

                session['user_id'] = new_user.user_id
                session['username'] = new_user.username
                session['permission'] = new_user.permissions

                return redirect('/')
            else:
                flash(u'Username already exists.', 'error')
                return render_template('auth/register.html', form=form)
        else:
            return render_template('auth/register.html', form=form)
    else:
        return redirect('/')
