from flask import Blueprint, render_template, redirect, url_for, request
from models import User, db

admin_bp = Blueprint('admin_bp', __name__, template_folder="templates")

@admin_bp.route("/admin")
def admin_dashboard():
    total_users = len(db.session.query(User).all())
    data = {
        "total_users":total_users
    }
    return render_template('admin/dashboard.html', context=data)


@admin_bp.route("/user-view-details")
def user_view_details():
    users = db.session.query(User).all()
    return render_template('admin/user_list.html', users = users)

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