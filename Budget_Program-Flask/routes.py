from flask import render_template, redirect, url_for, flash, request
import forms
from flask_paginate import Pagination, get_page_args
from flask_login import logout_user, login_user, login_required
import secrets
from PIL import Image
import smtplib
from email.message import EmailMessage
from flask_login import current_user
import os
from __init__ import app, db, bcrypt
from models import Vartotojas, PajamuIrasas, IslaiduIrasas
import logging
from email_settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER

@app.route("/registruotis", methods=['GET', 'POST'])
def registruotis():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegistracijosForma()
    try:
        if form.validate_on_submit():
            koduotas_slaptazodis = bcrypt.generate_password_hash(
                form.slaptazodis.data).decode('utf-8')
            vartotojas = Vartotojas(vardas=form.vardas.data,
                                    el_pastas=form.el_pastas.data,
                                    slaptazodis=koduotas_slaptazodis)
            db.session.add(vartotojas)
            db.session.commit()
            flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')
            return redirect(url_for('index'))
        return render_template('registruotis.html', title='Register', form=form)
    except Exception:
        flash('Toks vartotojas jau užregistruotas, bandykite kitą vardą ar el. paštą.', 'danger')
        return redirect(url_for('registruotis'))


@app.route("/prisijungti", methods=['GET', 'POST'])
def prisijungti():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis,
                                               form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('index'))
        else:
            flash('Prisijungti nepavyko. Patikrinkite el. paštą ir slaptažodį',
                  'danger')
    return render_template('prisijungti.html', title='Prisijungti', form=form)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.UzklausosAtnaujinimoForma()
    if form.validate_on_submit():
        try:
            user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
            send_reset_email(user)
            flash(
                'Jums išsiųstas el. laiškas su slaptažodžio atnaujinimo instrukcijomis.',
                'info')
            return redirect(url_for('prisijungti'))
        except Exception:
            flash('Tokio vartotojo sistemoje nėra.', 'danger')
            return redirect(url_for('reset_request'))
    return render_template('reset_request.html', title='Reset Password',
                           form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Vartotojas.verify_reset_token(token)
    if user is None:
        flash('Užklausa netinkama arba pasibaigusio galiojimo', 'warning')
        return redirect(url_for('reset_request'))
    form = forms.SlaptazodzioAtnaujinimoForma()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.slaptazodis.data).decode('utf-8')
        user.slaptazodis = hashed_password
        db.session.commit()
        flash('Tavo slaptažodis buvo atnaujintas! Gali prisijungti', 'success')
        return redirect(url_for('prisijungti'))
    return render_template('reset_token.html', title='Reset Password',
                           form=form)


@app.route("/paskyra", methods=['GET', 'POST'])
@login_required
def paskyra():
    form = forms.PaskyrosAtnaujinimoForma()
    if form.validate_on_submit():
        if form.nuotrauka.data:
            nuotrauka = save_picture(form.nuotrauka.data)
            current_user.nuotrauka = nuotrauka
        current_user.vardas = form.vardas.data
        current_user.el_pastas = form.el_pastas.data
        db.session.commit()
        flash('Tavo paskyra atnaujinta!', 'success')
        return redirect(url_for('paskyra'))
    elif request.method == 'GET':
        form.vardas.data = current_user.vardas
        form.el_pastas.data = current_user.el_pastas
    nuotrauka = url_for('static',
                        filename='profilio_nuotraukos/' + current_user.nuotrauka)
    return render_template('paskyra.html', title='Account', form=form,
                           nuotrauka=nuotrauka)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/pajamos", methods=['GET', 'POST'])
@login_required
def pajamos_in():
    vartotojas_id = current_user.id
    form = forms.P_Forma()
    if form.validate_on_submit():
        suma = form.suma.data
        kategorija = form.kategorija.data
        siuntejas = form.siuntejas.data
        papildoma_info = form.papildoma_info.data
        atsiskaitymas = form.atsiskaitymas.data
        isigyta = form.isigyta.data
        Biudzetas().ivesti_pajamas(int(suma), kategorija, siuntejas,
                                   papildoma_info, atsiskaitymas,
                                   isigyta, vartotojas_id)
        return render_template('pavyko.html', form=False)
    return render_template("pajamos.html", form=form)


@app.route("/islaidos", methods=['GET', 'POST'])
@login_required
def islaidos_in():
    form = forms.I_Forma()
    if form.validate_on_submit():
        suma = form.suma.data
        kategorija = form.kategorija.data
        vartotojas_id = current_user.id
        Biudzetas().ivesti_islaidas(int(suma), kategorija, vartotojas_id)
        return render_template('pavyko.html', form=False)
    return render_template("islaidos.html", form=form)


@app.route("/balansas", methods=['GET', 'POST'])
@login_required
def balansas():
    if request.method == "GET":
        try:
            bal = Biudzetas().gauti_balansa(vartotojas_id=current_user.id)
        except:
            bal = 0
        return render_template("balansas.html", data=bal)


def get_users(offset=0, per_page=5):
    return list[offset: offset + per_page]


@app.route("/ataskaita")
@login_required
def ataskaita():
    db.create_all()
    try:
        vartotojas_id = current_user.id
        ataskaita = Biudzetas().gauti_ataskaita(vartotojas_id)
    except:
        ataskaita = []
    global list
    list = []
    while True:
        try:
            list.append(next(ataskaita))
        except StopIteration:
            break
        except Exception:
            list.append('')
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(list)
    pagination_users = get_users(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('ataskaita.html',
                           list=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@app.route('/update_income/<int:id>', methods=['GET', 'POST'])
@login_required
def koreguoti_irasap(id):
    form = forms.P_Forma()
    p = db.session.query(PajamuIrasas).get(id)
    vartotojas_id = current_user.id
    if form.validate_on_submit():
        p.suma = form.suma.data
        p.kategorija = form.kategorija.data
        p.siuntejas = form.siuntejas.data
        p.papildoma_informacija = form.papildoma_info.data
        p.atsiskaitymo_budas = form.atsiskaitymas.data
        p.isigyta_preke_paslauga = form.isigyta.data
        db.session.commit()
        Biudzetas().koreguoti_pajamas(p.id, int(p.suma), p.kategorija,
                                      p.siuntejas,
                                      p.papildoma_informacija,
                                      p.atsiskaitymo_budas,
                                      p.isigyta_preke_paslauga, vartotojas_id)
        return render_template('pavyko.html', form=False)
    return render_template("korekcija_p.html", form=form, p=p)


@app.route('/update_outcome/<int:id>', methods=['GET', 'POST'])
@login_required
def koreguoti_irasai(id):
    form = forms.I_Forma()
    i = db.session.query(IslaiduIrasas).get(id)
    vartotojas_id = current_user.id
    if form.validate_on_submit():
        i.suma = form.suma.data
        i.kategorija = form.kategorija.data
        db.session.commit()
        Biudzetas().koreguoti_islaidas(i.id, int(i.suma), i.kategorija,
                                       vartotojas_id)
        return render_template('pavyko.html', form=False)
    return render_template("korekcija_i.html", form=form, i=i)


@app.route('/update/<int:id>/<string:tipas>', methods=['GET', 'POST'])
@login_required
def istrinti_irasa(id, tipas):
    vartotojas_id = current_user.id
    Biudzetas().istrinti_irasa(int(id), str(tipas), vartotojas_id)
    return render_template('pavyko.html')


@app.route("/trinti_viska", methods=['GET', 'POST'])
@login_required
def trinti_viska():
    vartotojas_id = current_user.id
    if request.method == "GET":
        try:
            trinti = Biudzetas().istrinti(vartotojas_id)
            return render_template("istrinti_viska.html", data=trinti)
        except Exception:
            return render_template("istrinti_viska.html")


@app.route("/baigti")
@login_required
def end():
    logout_user()
    return render_template('index.html')


@app.errorhandler(404)
def klaida_404(klaida):
    return render_template("404.html"), 404


@app.errorhandler(403)
def klaida_403(klaida):
    return render_template("403.html"), 403


@app.errorhandler(500)
def klaida_500(klaida):
    return render_template("500.html"), 500


class Biudzetas:
    def ivesti_pajamas(self, suma, kategorija, siuntejas,
                       papildoma_informacija, atsiskaitymo_budas,
                       isigyta_preke_paslauga, vartotojas_id):
        pajamos = PajamuIrasas(suma=suma, kategorija=kategorija,
                               siuntejas=siuntejas,
                               papildoma_informacija=papildoma_informacija,
                               atsiskaitymo_budas=atsiskaitymo_budas,
                               isigyta_preke_paslauga=isigyta_preke_paslauga,
                               vartotojas_id=vartotojas_id)
        logging.debug(
            f"I zurnala ivestos pajamos ir susijusi informacija: "
            f"Pajamu iraso ID: {pajamos.id}, suma: {pajamos.suma},  "
            f"kategorija: {pajamos.kategorija}, siuntejas: {pajamos.siuntejas},"
            f"papildoma informacija: {pajamos.papildoma_informacija},  "
            f"atsiskaitymo budas: {pajamos.atsiskaitymo_budas},  isigyta "
            f"preke ar paslauga: {pajamos.isigyta_preke_paslauga}")
        db.create_all()
        db.session.add(pajamos)
        db.session.commit()
        if Biudzetas().gauti_balansa(vartotojas_id) < 0:
            Biudzetas().send_mail()
        return pajamos

    def koreguoti_pajamas(self, ID, suma, kategorija, siuntejas,
                          papildoma_informacija, atsiskaitymo_budas,
                          isigyta_preke_paslauga, vartotojas_id):
        logging.debug(
            f"I zurnala ivestos koreguotos pajamos ir susijusi  "
            f"informacija: Pajamu iraso ID: {ID}, suma: {suma},  "
            f"kategorija: {kategorija}, siuntejas: {siuntejas},  "
            f"papildoma informacija: {papildoma_informacija},  "
            f"atsiskaitymo budas: {atsiskaitymo_budas},  isigyta "
            f"preke ar paslauga: {isigyta_preke_paslauga}")
        if Biudzetas().gauti_balansa(vartotojas_id) < 0:
            Biudzetas().send_mail()

    def ivesti_islaidas(self, suma, kategorija, vartotojas_id):
        islaidos = IslaiduIrasas(suma=suma, kategorija=kategorija,
                                 vartotojas_id=vartotojas_id)
        logging.debug(
            f"I zurnala ivestos islaidos ir susijusi  "
            f"informacija: Islaidu iraso ID: {islaidos.id}, suma: "
            f"{islaidos.suma}, kategorija: {islaidos.kategorija}")
        db.create_all()
        db.session.add(islaidos)
        db.session.commit()
        if Biudzetas().gauti_balansa(vartotojas_id) < 0:
            Biudzetas().send_mail()

    def koreguoti_islaidas(self, ID, suma, kategorija, vartotojas_id):
        logging.debug(
            f"I zurnala ivestos koreguotos islaidos ir susijusi informacija: "
            f"Islaidu iraso ID: {ID}, suma: {suma}, kategorija: "
            f" {kategorija}")
        if Biudzetas().gauti_balansa(vartotojas_id) < 0:
            Biudzetas().send_mail()

    def gauti_balansa(self, vartotojas_id):
        logging.debug("Iskviesta balanso funkcija")
        plistas = db.session.query(PajamuIrasas).filter_by(
            vartotojas_id=vartotojas_id).all()
        ilistas = db.session.query(IslaiduIrasas).filter_by(
            vartotojas_id=vartotojas_id).all()
        bal_suma = 0
        for i in plistas:
            bal_suma += i.suma
        for m in ilistas:
            bal_suma -= m.suma
        return bal_suma

    def gauti_ataskaita(self, vartotojas_id):
        logging.debug("Iskviesta ataskaitos funkcija")
        plistas = db.session.query(PajamuIrasas).filter_by(
            vartotojas_id=vartotojas_id).all()
        ilistas = db.session.query(IslaiduIrasas).filter_by(
            vartotojas_id=vartotojas_id).all()
        for i in plistas:
            yield i
        for m in ilistas:
            yield m

    def istrinti_irasa(self, ID, tipas, vartotojas_id):
        if tipas == 'PAJAMOS':
            plistas = db.session.query(PajamuIrasas).get(ID)
            db.session.delete(plistas)
            db.session.commit()
            logging.debug(f"Istrintas pajamu irasas {plistas.id}")

        if tipas == 'IŠLAIDOS':
            ilistas = db.session.query(IslaiduIrasas).get(ID)
            db.session.delete(ilistas)
            db.session.commit()
            logging.debug(f"Istrintas islaidu irasas {ilistas.id}")

        if Biudzetas().gauti_balansa(vartotojas_id) < 0:
            Biudzetas().send_mail()

    def istrinti(self, vartotojas_id):
        plistas = db.session.query(PajamuIrasas).filter_by(
            vartotojas_id=vartotojas_id).all()
        ilistas = db.session.query(IslaiduIrasas).filter_by(
            vartotojas_id=vartotojas_id).all()
        for i in plistas:
            db.session.delete(i)
            db.session.commit()
        for m in ilistas:
            db.session.delete(m)
            db.session.commit()
        logging.debug("Istrinti visi lenteliu duomenys")

    def send_mail(self):
        message = '''
            Dėmesio!
            Pranešame, kad balansas tapo neigiamas!
            '''
        email = EmailMessage()
        email['from'] = 'Vardas Pavardė'
        email['to'] = 'viskoniekas@gmail.com'
        email['subject'] = 'email from python'

        email.set_content(message)

        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            smtp.send_message(email)
        logging.debug("Issiustas el.laiskas su perspejimu, kad balansas  "
                      "tapo neigiamas")


def send_reset_email(user):
    token = user.get_reset_token()
    message = f'''
    Norėdami atnaujinti slaptažodį, paspauskite nuorodą:
    {url_for('reset_token', token=token, _external=True)} 
    Jei jūs nedarėte šios užklausos, nieko nedarykite ir slaptažodis nebus pakeistas.
     '''
    email = EmailMessage()
    email['from'] = 'Vardas Pavardė'
    email['to'] = [user.el_pastas]
    email['subject'] = 'Slaptažodžio keitimas'

    email.set_content(message)

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        smtp.send_message(email)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profilio_nuotraukos',
                                picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
