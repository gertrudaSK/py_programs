from flask_admin import Admin, BaseView, expose
from flask_mail import Mail
import logging
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from email_settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_USERNAME
from flask_admin.contrib.sqla import ModelView

logging.basicConfig(filename='logai_biudzeto.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
SECRET_KEY = os.urandom(33)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()

from models import Vartotojas, PajamuIrasas, IslaiduIrasas

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'prisijungti'
login_manager.login_message_category = 'info'
login_manager.login_message = "Reikalingas vartotojo prisijungimas."

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = EMAIL_USERNAME
app.config['MAIL_PASSWORD'] = EMAIL_HOST_PASSWORD

import routes


class ManoModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.el_pastas == EMAIL_HOST_USER


admin = Admin(app, name='EDIT', template_mode='bootstrap3')


class MyView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('index'))


admin.add_view(MyView(name='Biudžeto programa'))

admin.add_view(ManoModelView(PajamuIrasas, db.session))
admin.add_view(ManoModelView(IslaiduIrasas, db.session))
admin.add_view(ManoModelView(Vartotojas, db.session))


@login_manager.user_loader
def load_user(vartotojo_id):
    return Vartotojas.query.get(int(vartotojo_id))
