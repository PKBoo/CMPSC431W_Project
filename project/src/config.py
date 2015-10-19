DEBUG = True
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configuration
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/templatesandmoe'
DATABASE_CONNECT_OPTIONS = {}