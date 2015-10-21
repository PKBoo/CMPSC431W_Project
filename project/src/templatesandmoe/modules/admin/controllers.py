from flask import Blueprint, request, render_template, redirect, session
from templatesandmoe.modules.items.models import Item
adminModule = Blueprint('admin', __name__, url_prefix='/admin')


@adminModule.route('/', methods=['GET'])
def home():
    # Make sure user is logged in and is an admin
    if session.get('user_id') and session['permission'] > 0:
        return render_template("admin/home.html")
    else:
        return redirect("/")

@adminModule.route('/items', methods=['GET'])
def items():
	items = Item.get_all()
	print (items)
	return render_template("admin/items.html", items = items)