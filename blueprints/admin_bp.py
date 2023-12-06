from flask import Blueprint, render_template, redirect, url_for, request
from models import  db, User, Pet, Adoption, History

admin_bp = Blueprint('admin_bp', __name__, template_folder="templates")

@admin_bp.route("/admin")
def admin_dashboard():
    total_users = len(db.session.query(User).all())
    total_pets = len(db.session.query(Pet).all())
    adopted_pets = len(db.session.query(Adoption).filter_by(is_approved=True).all())
    data = {
        "total_users":total_users,
        "total_pets":total_pets,
        "adopted_pets":adopted_pets,
    }
    return render_template('admin/dashboard.html', context=data, title="Dashboard")


@admin_bp.route("/user-view-details")
def user_view_details():
    users = db.session.query(User).all()
    return render_template('admin/user_list.html', users = users, title="User List")

@admin_bp.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_bp.user_view_details'))

@admin_bp.route("/search_user", methods=["POST"])
def search_user():
    value = None
    if request.method == "POST":
        value = request.form.get("value")
        if value:
            users = db.session.query(User).filter(User.name.ilike(value)).all()
            return render_template("admin/user_list.html", users = users)
    return redirect(url_for("admin_bp.admin_dashboard"))

@admin_bp.route('/see-all-pets')
def see_all_pets():
    pets = db.session.query(Pet).all()
    return render_template('admin/pet_list.html', pets = pets, title="All Pets")

@admin_bp.route("/adoptions-history")
def history():
    histories = db.session.query(History).filter_by().all()
    
    return render_template('admin/history.html', title="History", histories=histories)

@admin_bp.route("/delete-history/<int:id>")
def delete_history(id):
    history = db.session.query(History).filter_by(id=id).first()
    db.session.delete(history)
    db.session.commit()
    return redirect(url_for('admin_bp.history'))


