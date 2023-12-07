from flask import Blueprint, redirect, render_template, url_for, request, session, current_app
from models import db, User, Pet, Adoption
import os

pet_bp = Blueprint('pet_bp', __name__, template_folder='templates')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@pet_bp.route('/add_pet', methods=["POST", "GET"])
def add_pet():
    if request.method == "POST":
        name = request.form.get("name")
        species = request.form.get("species")
        breed = request.form.get("breed")
        age = request.form.get("age")
        price = request.form.get("price")
        desc = request.form.get("desc")
        image = request.files.get("file")
        image_path = os.path.join(os.pardir ,current_app.config["UPLOAD_FOLDER"], image.filename)
        image.save(image_path)
        pet = Pet(owner_id = session.get("id"), name=name, species=species,
                  breed=breed, price=price, description=desc, age=age,image=image.filename)
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('pets/add_pet.html', title="Add Pet")

@pet_bp.route("/see_pets")
def see_pets():
    pets = db.session.query(Pet).filter_by(owner_id = session.get("id")).all()
    return render_template('pets/see_pets.html', pets=pets)



@pet_bp.route("/adopt-pet/<int:id>")
def adopt_pet(id):
    pet = db.session.query(Pet).filter_by(id=id).first()
    adopted = db.session.query(Adoption).filter_by(pet_id = pet.id, adopter_id=session.get("id")).first()
    if session.get("id") == pet.owner_id:
        return "<h1> You Can't adopt your own pet. </h1>"
    if not adopted:
        adoption = Adoption(pet_id = pet.id, owner_id=pet.owner_id, adopter_id=session.get("id"))
        db.session.add(adoption)
        db.session.commit()
    else:
        return "<h1> You Have Already Requested For this pet. </h1>"

    return redirect(url_for('home'))

@pet_bp.route("/search_pet", methods=["GET", "POST"])
def search_pet():
    search_val = None
    if request.method == "POST":
        search_val = request.form.get("search_val")
        if search_val:
            pets = db.session.query(Pet).filter(Pet.species.ilike(f"%{search_val}%")).all()
            return render_template("index.html", pets=pets, title="Searched Pet")
        
    return redirect(request.url)
