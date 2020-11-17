from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DateField
from wtforms.validators import InputRequired, Email


class RegistrationForm(FlaskForm):
    name = StringField('Name',  [InputRequired("Please enter your name.")])
    surname = StringField('Surname',  [InputRequired("Please enter your surname.")])
    birthday = DateField('Birthday YYYY-MM-DD', format='%Y-%m-%d')
    email = StringField('Email', [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    download = SubmitField('Download QR Code', render_kw={'class': 'btn btn-success'})
