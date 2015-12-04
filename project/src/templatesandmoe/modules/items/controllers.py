import os
from flask import Blueprint, request, render_template, redirect, session
from templatesandmoe.modules.core.pagination import Pagination
from templatesandmoe import db_session
from templatesandmoe.modules.items.service import ItemsService
from templatesandmoe.modules.categories.service import CategoriesService
from templatesandmoe.modules.ratings.service import RatingsService

itemsModule = Blueprint('items', __name__)
items = ItemsService(database=db_session)
categories = CategoriesService(database=db_session)
ratings = RatingsService(database=db_session)

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

        if user_rating:
            ratings.update_rating(item_id, session.get('user_id'), rating)
        else:
            ratings.add_rating(item_id, session.get('user_id'), rating)

        return redirect(request.referrer)
    else:
        return redirect('/login')
