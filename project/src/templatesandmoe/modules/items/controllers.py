from flask import abort, Blueprint, flash, request, render_template, redirect, session
from templatesandmoe.modules.core.pagination import Pagination
from templatesandmoe import db_session
from templatesandmoe.modules.items.service import ItemsService
from templatesandmoe.modules.categories.service import CategoriesService
from templatesandmoe.modules.ratings.service import RatingsService
from templatesandmoe.modules.auctions.service import AuctionsService

itemsModule = Blueprint('items', __name__)
items = ItemsService(database=db_session)
categories = CategoriesService(database=db_session)
ratings = RatingsService(database=db_session)
auctions = AuctionsService(database=db_session)

"""
    Show all templates
"""
@itemsModule.route('/templates/', defaults={ 'page': 1, 'category': 0 })
@itemsModule.route('/templates/<int:category>/page/<int:page>')
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


"""
    Show a single template
"""
@itemsModule.route('/templates/<int:item_id>')
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


"""
    Create or update a rating for a template
"""
@itemsModule.route('/templates/<int:item_id>/ratings', methods=['POST'])
def update_rating(item_id):
    if session.get('user_id'):
        rating = request.form.get('rating')
        user_rating = ratings.get_rating_for_template_by_user(item_id, session.get('user_id'))

        if user_rating is not None:
            ratings.update_rating(item_id, session.get('user_id'), rating)
        else:
            ratings.add_rating(item_id, session.get('user_id'), rating)

        return redirect(request.referrer)
    else:
        return redirect('/login')


"""
    Show all services
"""
@itemsModule.route('/services/', defaults={'page': 1})
@itemsModule.route('/services/page/<int:page>')
def services(page):
    auctions, count = items.get_filtered_services(page, services_per_page=15)
    pagination = Pagination(page, 15, count)

    return render_template('main/services.html',
                           auctions=auctions,
                           pagination=pagination)


"""
    Show single service
"""
@itemsModule.route('/services/<int:item_id>')
def single_service(item_id):
    service = items.get_service_by_id(item_id)
    if service is not None:
        bids = auctions.get_bids_for_service(service.service_id)
        has_ended = auctions.ended(service)

        return render_template('main/service.html',
                               service=service,
                               bids=bids,
                               has_ended=has_ended)
    else:
        abort(404)


"""
    Add a bid to a service
"""
@itemsModule.route('/services/<int:item_id>/bids', methods=['POST'])
def place_bid(item_id):
    user_id = session.get('user_id')
    amount = request.form.get('amount')

    if user_id:
        service = items.get_service_by_id(item_id)
        if not auctions.ended(service):
            highest_bid = auctions.get_highest_bid(service.service_id)

            if highest_bid is None:
                bid_check_amount = service.start_price
            else:
                bid_check_amount = highest_bid.amount

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
            flash('This auction has ended already.')
            return redirect(request.referrer)
    else:
        return redirect('/login')