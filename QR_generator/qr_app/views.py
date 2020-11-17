import os
from flask import render_template, send_from_directory, request
from qr_app import app
from .forms import RegistrationForm
import pyqrcode


def generate_qr(name, surname, birthday, email):
    qr_str = f'{name}\n{surname}\n{birthday}\n{email}'
    big_code = pyqrcode.create(qr_str, error='L', version=27,
                               mode='binary')
    big_code.png('MyCode.png', scale=6, module_color=[0, 0, 0, 128])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.surname.data
        birthday = form.birthday.data
        email = form.email.data
        generate_qr(name, surname, birthday, email)
        return send_from_directory(os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')),
            filename='MyCode.png',
            as_attachment=True)
    return render_template('registration.html', form=form)
