import os
from datetime import datetime
from threading import Thread
from flask import Flask, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from hashids import Hashids
from templatesandmoe.modules.auctions.manager import AuctionsManager

app = Flask(__name__)

# Load configuration options from config.py
app.config.from_object('config')

# Setup database
db = SQLAlchemy(app)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db.engine))

hashids = Hashids(salt='NTebZ10PhLdDM8EG00c7u14YGQW8PA0l', min_length=8)

auctions_manager = AuctionsManager(app=app, database=db_session)

# Import modules
from templatesandmoe.modules.main.controllers import mainModule as MainModule
from templatesandmoe.modules.items.controllers import itemsModule as ItemsModule
from templatesandmoe.modules.auth.controllers import authModule as AuthModule
from templatesandmoe.modules.admin.controllers import adminModule as AdminModule
from templatesandmoe.modules.api.controllers import apiModule as ApiModule

# Register modules
app.register_blueprint(MainModule)
app.register_blueprint(ItemsModule)
app.register_blueprint(AuthModule)
app.register_blueprint(AdminModule)
app.register_blueprint(ApiModule)


@app.teardown_request
def close_db_session(exception):
    db_session.close()


@app.before_first_request
def start_auction_manager():
    # Have to start auction manager after first connection is made for auto reload workaround
    t = Thread(target=auctions_manager.start)
    t.start()

# jinja template helper functions

# Returns a number as a USD currency
def currency_format(decimal):
    return '${:,.2f}'.format(decimal)


def format_rating(decimal):
    return '{:.1f}'.format(decimal)


# Return a datetime in 12 hour time
def time_format(time):
    return time.strftime('%m-%d-%Y %I:%M %p')


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    args.update(request.args)
    return url_for(request.endpoint, **args)


def template_preview_url(item_id):
    if os.path.isfile(app.config['TEMPLATES_DATA_PATH'] + '/' + str(item_id) + '/' + 'preview_' + str(item_id) + '.jpg'):
        return url_for(
            'static',
            filename='templates_data/' + str(item_id) + '/preview_' + str(item_id) + '.jpg'
        )
    else:
        return url_for('static', filename='images/default_preview.png')

app.jinja_env.globals['url_for_other_page'] = url_for_other_page
app.jinja_env.globals['currency_format'] = currency_format
app.jinja_env.globals['template_preview_url'] = template_preview_url
app.jinja_env.globals['time_format'] = time_format
app.jinja_env.globals['format_rating'] = format_rating
