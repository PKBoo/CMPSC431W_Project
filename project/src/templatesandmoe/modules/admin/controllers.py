import bcrypt
from flask import Blueprint, flash, render_template, redirect, request, session
from templatesandmoe import db_session
from templatesandmoe.modules.items.models import Item
from templatesandmoe.modules.users.models import User
from templatesandmoe.modules.users.service import UsersService
from templatesandmoe.modules.items.service import ItemsService
from templatesandmoe.modules.reporting.service import ReportingService
from templatesandmoe.modules.admin.forms.user import UserForm

adminModule = Blueprint('admin', __name__, url_prefix='/admin')
users_service = UsersService(database=db_session)
items_service = ItemsService(database=db_session)
reporting_service = ReportingService(database=db_session)


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
    _users = users_service.get_all()
    return render_template('admin/users.html', users=_users)


@adminModule.route('/users/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = users_service.get_by_id(user_id)

    # Make sure a user with this id actually exists
    if user is not None:
        form = UserForm(obj=user)

        # Check if we're submitting a form or not
        if form.validate_on_submit():
            # Only need to update the password if a new password was entered into the form
            if form.password.data:
                user.set_password(form.password.data)

            user.username = form.username.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.permissions = form.permissions.data
            user.save()

            flash(u'Successfully updated user.', 'success')
            return redirect('admin/users/' + str(user.user_id))
        else:
            templates = items_service.get_templates_by_user_id(user.user_id)
            services = items_service.get_services_by_user_id(user.user_id)
            return render_template('admin/edit_user.html',
                                   user=user,
                                   form=form,
                                   templates=templates,
                                   services=services)
    else:
        return redirect('/')


@adminModule.route('/users/add', methods=['GET', 'POST'])
def add_user():
    add_user_form = UserForm()
    if add_user_form.validate_on_submit():
        if users_service.exists(add_user_form.username.data):
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
    _items = items_service.get_all()
    _templates = items_service.get_all_templates()
    _services = items_service.get_all_services()

    return render_template('admin/items.html', templates=_templates, services=_services)

@adminModule.route('/reports')
def reports():
    period = request.args.get('period')
    total_revenue = reporting_service.total_revenue()
    total_transactions = reporting_service.total_transactions()
    total_won_bids = reporting_service.total_won_bids()
    all_items_sales_report = reporting_service.items_sales_report(period=period)

    return render_template('admin/reports.html',
                           period=period,
                           all_items_sales_report=all_items_sales_report,
                           total_revenue=total_revenue,
                           total_transactions=total_transactions,
                           total_won_bids=total_won_bids)