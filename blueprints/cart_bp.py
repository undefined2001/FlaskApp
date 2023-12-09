from flask import Blueprint, request, session, render_template, redirect, url_for
from models import db, Pet, User, Cart

cart_bp = Blueprint('cart_bp', __name__, template_folder="templates")

@cart_bp.route('/cart')
def view_cart():
    user_id = session.get("id")
    if user_id:
        carts = db.session.query(Cart).filter_by(buyer_id = user_id).all()
        total_price = 0
        for cart in carts:
            total_price += cart.pet.price
        return render_template('cart/cart.html', carts = carts, total_price=total_price)
    return redirect(url_for('home'))

'''
class Cart(db.Model):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True, nullable=False)
    pet_id = Column(ForeignKey('pets.id'), nullable=False)
    buyer_id = Column(ForeignKey('users.id'), nullable=False)
    total_price = Column(Integer, nullable=False)

'''

@cart_bp.route('/add-to-cart/<int:id>')
def add_to_cart(id):
    pet = db.session.query(Pet).filter_by(id=id).first()
    user_id = session.get("id")
    if user_id and pet:
        if not db.session.query(Cart).filter_by(pet_id=pet.id, buyer_id=user_id).first():
            cart = Cart(pet_id=pet.id, buyer_id=user_id)
            db.session.add(cart)
            db.session.commit()
            return "Added Successfully"
    return "Can't Added the same pet twice"

@cart_bp.route("/remove-from-cart/<int:id>")
def remove_from_cart(id):
    cart = db.session.query(Cart).filter_by(id = id).first()
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('cart_bp.view_cart'))