from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import cloudinary

app = Flask(__name__)
app.secret_key = '6Sjksbfbjn^*^*UJ15^*&*&%4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/phongmach?charset=utf8mb4' % quote('huynhanhtuan')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['KETOA_KEY'] = 'ketoa'

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name='hat',
    api_key='262655147657561',
    api_secret='6GqTH9RFellUmTBFjAEF0KnAIFk'
)

login = LoginManager(app=app)