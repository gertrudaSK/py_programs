from flask_admin import Admin
from flask_mail import Mail
from flask_bcrypt import Bcrypt
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_USERNAME, \
    SECRET_KEY
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect, url_for
from flask_login import current_user

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_name=os.getenv('FLASK_CONFIG')):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    app.config['SECRET_KEY'] = SECRET_KEY

    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'sign_in'
    login_manager.login_message_category = 'info'
    login_manager.login_message = "You need to sign up!"

    mail.init_app(app)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = EMAIL_USERNAME
    app.config['MAIL_PASSWORD'] = EMAIL_HOST_PASSWORD
    migrate = Migrate(app, db)
    return app


app = create_app()
admin = Admin(app, name='Utilities Calculator', template_mode='bootstrap3')

from .models import Service, ApartmentStatus, ReportStatus, User, \
    House, \
    Apartment, Renter, ServiceCost, Electricity, Gas, ServiceCost, \
    HotWater, \
    ColdWater, OtherUtilities, Rent


def insert_data():
    check_rows = Service.query.all()
    if len(check_rows) == 0:
        with app.app_context():
            db.session.add(ApartmentStatus(status='RENT'))
            db.session.add(ApartmentStatus(status='MAIN'))
            db.session.add(ReportStatus(status='YES'))
            db.session.add(ReportStatus(status='NO'))
            db.session.add(Service('Electricity'))
            db.session.add(Service('Gas'))
            db.session.add(Service('Hot Water'))
            db.session.add(Service('Cold Water'))
            db.session.add(Service('Rent'))
            db.session.add(Service('Other Utilities'))
            db.session.commit()


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('home'))


def admin_create():
    admin.add_view(MyView(name='Back to Page'))
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(House, db.session))
    admin.add_view(MyModelView(Apartment, db.session))
    admin.add_view(MyModelView(Renter, db.session))
    admin.add_view(MyModelView(Service, db.session))
    admin.add_view(MyModelView(ServiceCost, db.session))
    admin.add_view(MyModelView(Electricity, db.session))
    admin.add_view(MyModelView(Gas, db.session))
    admin.add_view(MyModelView(HotWater, db.session))
    admin.add_view(MyModelView(ColdWater, db.session))
    admin.add_view(MyModelView(OtherUtilities, db.session))
    admin.add_view(MyModelView(Rent, db.session))


from . import views
