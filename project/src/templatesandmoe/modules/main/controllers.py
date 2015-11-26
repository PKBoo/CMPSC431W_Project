from flask import Blueprint, request, render_template, redirect, session
from templatesandmoe import db_session
from templatesandmoe.modules.items.service import ItemsService
from templatesandmoe.modules.main.forms.payment_information import PaymentInformationForm


mainModule = Blueprint('main', __name__)
items = ItemsService(database=db_session)


@mainModule.route('/', methods=['GET'])
def home():
    latest_templates = items.get_latest_templates(4)
    return render_template("main/home.html", latest_templates=latest_templates)


@mainModule.route('/order/template/<int:item_id>', methods=['GET', 'POST'])
def order_item(item_id):
    if session.get('user_id'):
        template = items.get_template_by_id(item_id)

        if template is not None:
            payment_form = PaymentInformationForm()

            if payment_form.validate_on_submit():
                return 'hello'
            else:
                return render_template('main/order.html', template=template, form=payment_form)
        else:
            return redirect('/')
    else:
        return redirect('/login')
