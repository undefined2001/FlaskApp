from flask import Blueprint, render_template, request, redirect, session, url_for
from models import db, User, Pet, Adoption, History

user_bp = Blueprint('user_bp', __name__, template_folder="templates")

@user_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        user = User(name = name, email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_bp.login'))
    return render_template('register.html', title="register")

@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.session.query(User).filter_by(email=email).first()
        if user and user.check_password(password):
            session["id"] = user.id
            if user.role == "admin":
                return redirect(url_for('admin_bp.admin_dashboard'))
            return redirect(url_for('home'))
        else:
            return "<h1>Invalid email or password</h1>"
    return render_template('login.html', title="Login")


@user_bp.route('/logout')
def logout():
    session.pop("id")
    return redirect(url_for("user_bp.login"))


@user_bp.route("/see-request")
def request_status():
    requests = db.session.query(Adoption).filter_by(adopter_id = session.get("id")).all()
    return render_template("request_list.html", title="Request List", requests = requests)


@user_bp.route("/see-your-request")
def pending_request_status():
    requests = db.session.query(Adoption).filter_by(owner_id = session.get("id"), is_approved = False).all()
    for req in requests:
        print(req)
    return render_template("pending_request.html", title="Pending Request List", requests = requests)

@user_bp.route("/approve-request/<int:id>")
def approve_request(id):
    req = db.session.query(Adoption).filter_by(id=id).first()
    req.is_approved = True
    db.session.add(req)
    seller = db.session.query(User).filter_by(id = req.owner_id).first()
    buyer = db.session.query(User).filter_by(id = req.adopter_id).first()
    history = History(seller_id=seller.id, buyer_id=buyer.id, pet=req.pet, type="Adoption")
    db.session.add(history)
    db.session.commit()
    return redirect(url_for('user_bp.pending_request_status'))


@user_bp.route("/decline-request/<int:id>")
def decline_request(id):
    req = db.session.query(Adoption).filter_by(id=id).first()
    
    db.session.delete(req)
    db.session.commit()
    return redirect(url_for('user_bp.pending_request_status'))