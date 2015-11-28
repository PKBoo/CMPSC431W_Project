from flask import Blueprint, request, render_template, redirect, session
from templatesandmoe.modules.core.pagination import Pagination
from templatesandmoe import db_session, hashids
from templatesandmoe.modules.items.service import ItemsService
from templatesandmoe.modules.main.forms.payment_information import PaymentInformationForm
from templatesandmoe.modules.orders.service import OrdersService
from templatesandmoe.modules.orders.models import CardPayment

mainModule = Blueprint('main', __name__)
items = ItemsService(database=db_session)
orders = OrdersService(database=db_session)


@mainModule.route('/', methods=['GET'])
def home():
    latest_templates = items.get_latest_templates(4)
    return render_template("main/home.html", latest_templates=latest_templates)


@mainModule.route('/orders/<string:transaction_id>', methods=['GET'])
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


@mainModule.route('/templates/', defaults={ 'page': 1 })
@mainModule.route('/templates/page/<int:page>')
def all_templates(page):
    templates = items.get_filtered_templates(page=page)
    pagination = Pagination(page, 16, items.templates_count())
    return render_template('main/templates.html', templates=templates, pagination=pagination)