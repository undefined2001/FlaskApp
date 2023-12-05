from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    password:Mapped[str] = mapped_column(String(128), nullable=True)
    role:Mapped[str] = mapped_column(String(10), nullable=True)

    def set_password(self, password):
        hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashpass

    def check_password(self, password):
        res = bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        return res

class Pet(db.Model):
    __tablename__ = 'pets'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id:Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    image:Mapped[str] = mapped_column(String(250), nullable=True)
    name:Mapped[str] = mapped_column(String(20), nullable=False)
    species:Mapped[str] = mapped_column(String(20), nullable=False)
    breed:Mapped[str] = mapped_column(String(30), nullable=True)
    age:Mapped[str] = mapped_column(String(50), nullable=False)
    price:Mapped[float] = mapped_column(Float, nullable=True, default=0.0)
    description:Mapped[str] = mapped_column(Text, nullable=True)

    