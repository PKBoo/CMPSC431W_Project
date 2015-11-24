from flask import Blueprint, request, render_template
from templatesandmoe import db_session
from templatesandmoe.modules.items.service import ItemsService

mainModule = Blueprint('main', __name__, url_prefix='/')
items = ItemsService(database=db_session)

@mainModule.route('/', methods=['GET'])
def home():
    latest_templates = items.get_latest_templates(4)
    return render_template("main/home.html", latest_templates=latest_templates)