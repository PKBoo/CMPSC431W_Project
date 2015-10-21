from flask import Blueprint, request, render_template, redirect, session
from templatesandmoe.modules.items.models import Item
adminModule = Blueprint('admin', __name__, url_prefix='/admin')


@adminModule.before_request
def before_request():
    # Make sure user is logged in and is an admin
    if session.get('user_id') and session['permission'] > 0:
        pass
    else:
        return redirect("/")

@adminModule.route('/', methods=['GET'])
def home():
    return render_template("admin/home.html")

@adminModule.route('/items', methods=['GET'])
def items():
    items = Item.get_all()
    return render_template("admin/items.html", items = items)