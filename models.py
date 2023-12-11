from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class History(db.Model):
    __tablename__ = 'histories'
    id = Column(Integer, primary_key=True)
    seller_id = Column(ForeignKey('users.id'), nullable=False)
    buyer_id = Column(ForeignKey('users.id'), nullable=False)
    pet_id = Column(ForeignKey('pets.id'), nullable=False)
    type = Column(String(10), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)

class BuyingHistory(db.Model):
    __tablename__ = 'buying_history'
    id = Column(Integer, primary_key=True, nullable=False)
    total_amount = Column(Integer, nullable=False)
    buyer = Column(ForeignKey('users.id'), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)

    

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    name = Column(String(30), nullable=False)
    phone = Column(String(15), nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(String(10), nullable=True)
    pet = relationship('Pet', backref='owner', lazy=True)
    buyer = relationship('History', backref='buyer', foreign_keys=[History.buyer_id], lazy=True)
    seller = relationship('History', backref='seller', foreign_keys=[History.seller_id], lazy=True)
    buyer_bh = relationship("BuyingHistory", backref='hbuyer',foreign_keys=[BuyingHistory.buyer], lazy=True)
    buyer_c = relationship('Cart', backref='buyer',  lazy=True)

    def set_password(self, password):
        hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashpass

    def check_password(self, password):
        res = bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        return res

class Pet(db.Model):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    image = Column(String(250), nullable=True)
    name = Column(String(20), nullable=False)
    species = Column(String(20), nullable=False)
    breed = Column(String(30), nullable=True)
    age = Column(String(50), nullable=False)
    price = Column(Float, nullable=True, default=0.0)
    description = Column(Text, nullable=True)
    pet_a = relationship('Adoption', backref='pet', lazy=True)
    pet_h = relationship('History', backref='pet', lazy=True)
    pet_c = relationship('Cart', backref='pet', lazy=True)

class Adoption(db.Model):
    __tablename__ = 'adoptions'
    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey('users.id'), nullable=False)
    pet_id = Column(ForeignKey('pets.id'), nullable=False)
    adopter_id = Column(ForeignKey('users.id'), nullable=False)
    is_approved = Column(Boolean, nullable=False, default=False)
    date = Column(DateTime, default=datetime.utcnow)

class Cart(db.Model):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True, nullable=False)
    pet_id = Column(ForeignKey('pets.id'), nullable=False)
    buyer_id = Column(ForeignKey('users.id'), nullable=False)
    is_sold = Column(Boolean, default=False)

    



