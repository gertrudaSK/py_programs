from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from __init__ import db, app


class Vartotojas(db.Model, UserMixin):
    __tablename__ = "vartotojas"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String(20), unique=True, nullable=False)
    el_pastas = db.Column("El. pašto adresas", db.String(120), unique=True,
                          nullable=False)
    nuotrauka = db.Column(db.String(20), nullable=False, default='default.jpg')
    slaptazodis = db.Column("Slaptažodis", db.String(60), unique=True,
                            nullable=False)
    pajamos = relationship('PajamuIrasas')
    islaidos = relationship('IslaiduIrasas')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Vartotojas.query.get(user_id)


class Irasas:

    def __init__(self, suma, kategorija):
        self.suma = suma
        self.kategorija = kategorija


class PajamuIrasas(Irasas, db.Model):
    __tablename__ = "PAJAMOS"

    id = db.Column(db.Integer, primary_key=True)
    suma = db.Column(db.Integer, nullable=False)
    kategorija = db.Column(db.String, nullable=False)
    siuntejas = db.Column(db.String, nullable=False)
    papildoma_informacija = db.Column(db.String, nullable=False)
    atsiskaitymo_budas = db.Column(db.String, nullable=False)
    isigyta_preke_paslauga = db.Column(db.String, nullable=False)
    laikas = db.Column(db.String, default=datetime.strftime(datetime.now(),
                                                            "%Y-%m-%d %H:%M"))
    tipas = db.Column(db.String, default="PAJAMOS")
    vartotojas_id = Column(Integer, ForeignKey("vartotojas.id"))
    vartotojas = relationship('Vartotojas')

    def __init__(self, suma, kategorija, siuntejas, papildoma_informacija,
                 atsiskaitymo_budas, isigyta_preke_paslauga, vartotojas_id):
        super().__init__(suma, kategorija)
        self.siuntejas = siuntejas
        self.papildoma_informacija = papildoma_informacija
        self.atsiskaitymo_budas = atsiskaitymo_budas
        self.isigyta_preke_paslauga = isigyta_preke_paslauga
        self.vartotojas_id = vartotojas_id

    def __repr__(self):
        return f"Pajamų įrašo ID: {self.id}, suma:" \
               f" {self.suma}, kategorija:" \
               f" {self.kategorija}, įvedimo data: {self.laikas}, siuntėjas:" \
               f" {self.siuntejas}, papildoma informacija:" \
               f" {self.papildoma_informacija}, atsiskaitymo būdas:" \
               f" {self.atsiskaitymo_budas}, įsigyta prekė ar paslauga:" \
               f" {self.isigyta_preke_paslauga}"


class IslaiduIrasas(Irasas, db.Model):
    __tablename__ = "ISLAIDOS"

    id = Column(Integer, primary_key=True)
    suma = Column("Suma", Integer)
    kategorija = Column("Kategorija", String)
    laikas = db.Column(db.String, default=datetime.strftime(datetime.now(),
                                                            "%Y-%m-%d %H:%M"))
    tipas = db.Column(db.String, default="IŠLAIDOS")
    vartotojas_id = Column(Integer, ForeignKey("vartotojas.id"))
    vartotojas = relationship('Vartotojas')

    def __init__(self, suma, kategorija, vartotojas_id):
        super().__init__(suma, kategorija)
        self.vartotojas_id = vartotojas_id

    def __repr__(self):
        return f"Išlaidų įrašo ID: {self.id}, suma: {self.suma}," \
               f" kategorija: {self.kategorija}, įvedimo data: {self.laikas}"
