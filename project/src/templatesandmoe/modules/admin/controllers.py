import bcrypt
from flask import Blueprint, flash, render_template, redirect, session
from templatesandmoe.modules.items.models import Item
from templatesandmoe.modules.users.models import User
from templatesandmoe.modules.admin.forms.add_user import AddUserForm

adminModule = Blueprint('admin', __name__, url_prefix='/admin')


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
    _users = User.get_all()
    return render_template('admin/users.html', users=_users)


@adminModule.route('/users/add', methods=['GET', 'POST'])
def add_user():
    add_user_form = AddUserForm()
    if add_user_form.validate_on_submit():
        password = add_user_form.password.data.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        new_user = User(username=add_user_form.username.data,
                        password=hashed_password,
                        first_name=add_user_form.first_name.data,
                        last_name=add_user_form.last_name.data,
                        email=add_user_form.email.data,
                        permissions=add_user_form.permission.data)
        new_user.create()
        flash(u'Successfully added user.', 'success')

        return redirect('admin/users/add')
    else:
        return render_template('admin/add_user.html', form=add_user_form)


@adminModule.route('/items', methods=['GET'])
def items():
    _items = Item.get_all()
    return render_template('admin/items.html', items = _items)