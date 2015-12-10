import os
from flask import Blueprint, request, render_template, redirect, session, flash
from config import TEMPLATES_DATA_PATH
from templatesandmoe import db_session, hashids
from templatesandmoe.modules.items.service import ItemsService
from templatesandmoe.modules.items.forms import AddTemplateForm, AddServiceForm
from templatesandmoe.modules.main.forms.payment_information import PaymentInformationForm
from templatesandmoe.modules.orders.service import OrdersService
from templatesandmoe.modules.orders.models import CardPayment
from templatesandmoe.modules.categories.service import CategoriesService
from templatesandmoe.modules.auctions.service import AuctionsService
from templatesandmoe.modules.tags.service import TagsService
from templatesandmoe.modules.users.service import UsersService
from templatesandmoe.modules.reporting.service import ReportingService

mainModule = Blueprint('main', __name__)
items = ItemsService(database=db_session)
orders = OrdersService(database=db_session)
categories = CategoriesService(database=db_session)
auctions = AuctionsService(database=db_session)
tags = TagsService(database=db_session)
users = UsersService(database=db_session)
reports = ReportingService(database=db_session)


@mainModule.route('/', methods=['GET'])
def home():
    latest_templates = items.get_latest_templates(4)
    return render_template("main/home.html", latest_templates=latest_templates)


@mainModule.route('/account')
def account():
    if session.get('user_id'):
        user_id = session.get('user_id')
        users_bid_services = auctions.get_services_user_bid_on(user_id)
        won_bids = auctions.get_won_bids_by_user(user_id)
        users_services = items.get_services_by_user_id(user_id)

        return render_template("main/account.html",
                               users_bid_services=users_bid_services,
                               won_bids=won_bids,
                               users_services=users_services)
    else:
        return redirect('/login')


@mainModule.route('/account/templates')
def account_templates():
    user_id = session.get('user_id')
    if user_id:
        templates = reports.item_sales_report_for_user(user_id)

        return render_template('main/account_items.html',
                               items=templates)
    else:
        return redirect('/login')


@mainModule.route('/account/orders')
def account_orders():
    if session.get('user_id'):
        templates = orders.get_orders_by_user(session.get('user_id'))

        return render_template('main/account_orders.html',
                               orders=templates)
    else:
        return redirect('/login')


@mainModule.route('/orders/<string:transaction_id>')
def order_summary(transaction_id):
    decoded_id = hashids.decode(transaction_id)
    transaction = orders.get_order_by_id(decoded_id)

    # make sure the currently logged in user owns this order
    if transaction[0].user_id == session.get('user_id'):
        return render_template('main/order_summary.html', transaction=transaction, order_id=transaction_id)
    else:
        return redirect('/login')


@mainModule.route('/order/template/<int:item_id>', methods=['GET', 'POST'])
def order_item(item_id):
    if session.get('user_id'):
        template = items.get_template_by_id(item_id)

        if template is not None:
            payment_form = PaymentInformationForm()

            if payment_form.validate_on_submit():
                card = CardPayment(payment_form.name.data,
                                   payment_form.number.data,
                                   payment_form.expiration_month.data,
                                   payment_form.expiration_year.data,
                                   payment_form.cvc.data)
                transaction_id = orders.create_order(session.get('user_id'), card, [template.item_id])
                encoded_transaction_id = hashids.encode(transaction_id)
                return redirect('/orders/' + encoded_transaction_id)
            else:
                return render_template('main/order.html', template=template, form=payment_form)
        else:
            return redirect('/')
    else:
        return redirect('/login')


@mainModule.route('/sell/template', methods=['GET', 'POST'])
def sell_template():
    if session.get('user_id'):
        template_form = AddTemplateForm()

        all_categories = categories.get_all()
        categories_select_datasource = []
        for cat in all_categories:
            categories_select_datasource.append((cat.category_id, cat.name))
        template_form.category.choices = categories_select_datasource

        all_tags = tags.get_all()

        if template_form.validate_on_submit():

            # Insert the template into the database, then create a folder for it in templates_data
            try:
                item_id = items.add_template(
                    session.get('user_id'),
                    template_form.name.data,
                    template_form.price.data,
                    template_form.description.data,
                    template_form.category.data)

                tags.create_custom_tags_for_item(template_form.custom_tags.data.split(','), item_id)
                tags.add_tags_to_item(template_form.tags.data.split(','), item_id)

                data_folder = TEMPLATES_DATA_PATH + '/' + str(item_id) + '/'
                os.makedirs(data_folder)

                # Create preview image from uploaded file
                preview_data = request.files[template_form.preview.name].read()
                open(os.path.join(data_folder, 'preview_' + str(item_id) + '.jpg'), 'wb').write(preview_data)

                # Create zip file from uploaded file
                files_data = request.files[template_form.files.name].read()
                open(os.path.join(data_folder, 'download_' + str(item_id) + '.zip'), 'wb').write(files_data)

                return redirect('/templates/' + str(item_id))
            except Exception as e:
                print(e)
                return 'Something terrible happened.'
        else:
            return render_template('main/sell_template.html', template_form=template_form, all_tags=all_tags)
    else:
        return redirect('/login')


@mainModule.route('/sell/service', methods=['GET', 'POST'])
def sell_service():

    if session.get('user_id'):
        service_form = AddServiceForm()

        if service_form.validate_on_submit():
            try:
                item_id = items.add_service(session.get('user_id'),
                                            service_form.name.data,
                                            service_form.start_price.data,
                                            service_form.description.data,
                                            service_form.duration.data)

                return redirect('/services/' + str(item_id))
            except Exception as e:
                print(e)
                return 'Something terrible happened.'
        else:
            return render_template('main/sell_service.html', service_form=service_form)
    else:
        return redirect('/login')


@mainModule.route('/user/<string:username>')
def user_profile(username):
    user=users.get_by_username(username)
    if user is None:
        return redirect('/')

    user_id=user.user_id
    user_templates=items.get_templates_by_user_id(user_id)
    user_services=items.get_services_by_user_id(user_id)
    user_avg_rating=users.get_average_template_rating(user_id)


    return render_template('main/user.html', user=user, templates=user_templates, rating=user_avg_rating, services=user_services)