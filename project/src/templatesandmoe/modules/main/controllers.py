import os
from flask import Blueprint, request, render_template, redirect, session, flash
from config import TEMPLATES_DATA_PATH
from templatesandmoe.modules.core.pagination import Pagination
from templatesandmoe import db_session, hashids
from templatesandmoe.modules.items.service import ItemsService
from templatesandmoe.modules.items.forms import AddTemplateForm, AddServiceForm
from templatesandmoe.modules.main.forms.payment_information import PaymentInformationForm
from templatesandmoe.modules.orders.service import OrdersService
from templatesandmoe.modules.orders.models import CardPayment
from templatesandmoe.modules.categories.service import CategoriesService
from templatesandmoe.modules.ratings.service import RatingsService
from templatesandmoe.modules.auctions.service import AuctionsService

mainModule = Blueprint('main', __name__)
items = ItemsService(database=db_session)
orders = OrdersService(database=db_session)
categories = CategoriesService(database=db_session)
ratings = RatingsService(database=db_session)
auctions = AuctionsService(database=db_session)

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


@mainModule.route('/templates/', defaults={ 'page': 1, 'category': 0 })
@mainModule.route('/templates/<int:category>/page/<int:page>')
def all_templates(category, page):
    price_start = request.args.get('price-start')
    price_end = request.args.get('price-end')
    search = request.args.get('search')

    templates, count = items.get_filtered_templates(page=page,
                                                    templates_per_page=15,
                                                    category=category,
                                                    price_start=price_start,
                                                    price_end=price_end,
                                                    search=search)
    pagination = Pagination(page, 15, count)
    child_categories = categories.get_children(root_category=category)

    breadcrumb = None
    if category > 0:
        breadcrumb = categories.get_path_to_root(category)

    return render_template('main/templates.html',
                           templates=templates,
                           pagination=pagination,
                           categories=child_categories,
                           breadcrumb=breadcrumb,
                           category=category,
                           price_start=price_start,
                           price_end=price_end,
                           search=search)


@mainModule.route('/templates/<int:item_id>')
def single_template(item_id):
    template = items.get_template_by_id(item_id)
    breadcrumb = categories.get_path_to_root(template.category_id)
    rating = ratings.get_average_by_template_id(template.template_id)

    # if the user is logged in, determine if they have already rated this template.
    user_rating = None
    if session.get('user_id'):
        user_rating = ratings.get_rating_for_template_by_user(template.template_id, session.get('user_id'))

    return render_template('main/template.html',
                           breadcrumb=breadcrumb,
                           template=template,
                           rating=rating,
                           user_rating=user_rating)


@mainModule.route('/templates/<int:item_id>/ratings', methods=['POST'])
def update_rating(item_id):
    if session.get('user_id'):
        rating = request.form.get('rating')
        user_rating = ratings.get_rating_for_template_by_user(item_id, session.get('user_id'))

        if user_rating:
            ratings.update_rating(item_id, session.get('user_id'), rating)
        else:
            ratings.add_rating(item_id, session.get('user_id'), rating)

        return redirect(request.referrer)
    else:
        return redirect('/login')


@mainModule.route('/sell', methods=['GET', 'POST'])
def sell():
    if session.get('user_id'):
        template_form = AddTemplateForm()
        service_form = AddServiceForm()

        all_categories = categories.get_all()
        categories_select_datasource = []
        for cat in all_categories:
            categories_select_datasource.append((cat.category_id, cat.name))
        template_form.category.choices = categories_select_datasource

        return render_template('main/sell.html', template_form=template_form, service_form=service_form)
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

        if template_form.validate_on_submit():
            # Insert the template into the database, then create a folder for it in templates_data
            try:
                item_id = items.add_template(
                    session.get('user_id'),
                    template_form.name.data,
                    template_form.price.data,
                    template_form.description.data,
                    template_form.category.data)

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
            return render_template('main/sell_template.html', template_form=template_form)
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
                                            service_form.end_date.data)

                return redirect('/services/' + str(item_id))
            except Exception as e:
                print(e)
                return 'Something terrible happened.'
        else:
            return render_template('main/sell_service.html', service_form=service_form)
    else:
        return redirect('/login')

@mainModule.route('/services/', defaults={'page': 1})
@mainModule.route('/services/page/<int:page>')
def services(page):
    auctions, count = items.get_filtered_services(page, services_per_page=15)
    pagination = Pagination(page, 15, count)
    return render_template('main/services.html',
                           auctions=auctions,
                           pagination=pagination)


@mainModule.route('/services/<int:item_id>')
def single_service(item_id):
    service = items.get_service_by_id(item_id)
    bids = auctions.get_bids_for_service(service.service_id)
    return render_template('main/service.html',
                           service=service,
                           bids=bids)


@mainModule.route('/services/<int:item_id>/bids', methods=['POST'])
def place_bid(item_id):
    user_id = session.get('user_id')
    amount = request.form.get('amount')
    if user_id:

        service = items.get_service_by_id(item_id)
        highest_bid = auctions.get_highest_bid(service.service_id)
        bid_check_amount = highest_bid.amount
        if highest_bid is None:
            bid_check_amount = service.start_price

        # Make sure bid amount is a valid currency amount
        try:
            amount = float("{0:.2f}".format(float(amount)))
        except:
            flash('Bid must be a valid amount.', category='bid')
            return redirect(request.referrer)

        # Don't allow bidding if current user is the owner of the service
        # or if the current user is currently the highest bidder (only if bids exist)
        if service.user_id != user_id and (highest_bid is None or highest_bid.user_id != user_id):

            # if there is a highest bid, make sure the bid amount is greater than it
            if amount > bid_check_amount:
                auctions.place_bid(service.service_id, user_id, amount)
                flash('Successfully placed bid', category='bid_placed')
                return redirect(request.referrer)
            else:
                flash('Bid amount must be greater than highest bid.', category='bid')
                return redirect(request.referrer)
        else:
            flash('You already have the highest bid.', category='bid')
            return redirect(request.referrer)
    else:
        return redirect('/login')