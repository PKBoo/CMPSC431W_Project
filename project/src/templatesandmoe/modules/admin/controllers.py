import bcrypt
from flask import Blueprint, flash, render_template, redirect, session
from templatesandmoe import db_session
from templatesandmoe.modules.items.models import Item
from templatesandmoe.modules.users.models import User
from templatesandmoe.modules.users.service import UserService
from templatesandmoe.modules.admin.forms.user import UserForm

adminModule = Blueprint('admin', __name__, url_prefix='/admin')
user_service = UserService(database=db_session)

@adminModule.before_request
def before_request():
    # Make sure user is logged in and is an admin
    if session.get('user_id') and session['permission'] > 0:
        pass
    else:
        return redirect('/')


@adminModule.route('/', methods=['GET'])
def home():
    return render_template('admin/home.html')


@adminModule.route('/users', methods=['GET'])
def users():
    _users = user_service.get_all()
    return render_template('admin/users.html', users=_users)


@adminModule.route('/users/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = user_service.get_by_id(user_id)
    if user is not None:
        form = UserForm(obj=user)
        #if form.validate_on_submit():

        # else:
        #
        return render_template('admin/edit_user.html', user=user, form=form)
    else:
        return redirect('/')


@adminModule.route('/users/add', methods=['GET', 'POST'])
def add_user():
    add_user_form = UserForm()
    if add_user_form.validate_on_submit():
        if user_service.exists(add_user_form.username.data):
            flash(u'Username already exists.', 'error')
        else:
            password = add_user_form.password.data.encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            new_user = User(username=add_user_form.username.data,
                            password=hashed_password,
                            first_name=add_user_form.first_name.data,
                            last_name=add_user_form.last_name.data,
                            email=add_user_form.email.data,
                            permissions=add_user_form.permissions.data)

            new_user.create()
            flash(u'Successfully added user.', 'success')

        return redirect('admin/users/add')
    else:
        return render_template('admin/add_user.html', form=add_user_form)


@adminModule.route('/items', methods=['GET'])
def items():
    _items = Item.get_all()
    return render_template('admin/items.html', items = _items)