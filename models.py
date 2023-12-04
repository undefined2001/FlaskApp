from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
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
