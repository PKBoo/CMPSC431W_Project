from flask import Blueprint, request, render_template, redirect, session

adminModule = Blueprint('admin', __name__, url_prefix='/admin')


@adminModule.route('/', methods=['GET'])
def home():
    # Make sure user is logged in and is an admin
    if session.get('user_id') and session['permission'] > 0:
        return render_template("admin/home.html")
    else:
        return redirect("/")