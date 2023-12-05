from flask import Flask, render_template, request, redirect, url_for, session
from models import User, db
from blueprints import admin_bp, pet_bp
import os

app = Flask(__name__)
app.register_blueprint(admin_bp)
app.register_blueprint(pet_bp)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://mysql:root@localhost:3306/flaskapp"
app.config["SECRET_KEY"] = "Asraful"
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'media')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


db.init_app(app)

@app.context_processor
def is_admin():
    user = db.session.query(User).filter_by(id = session.get("id")).first()
    if user and user.role:
        return {'is_admin':True}
    else:
        return {'is_admin':False}
    
@app.context_processor
def is_loggedin():
    if session.get("id"):
        return {'is_loggedin':True}
    else:
        return {'is_loggedin':False}

@app.route("/")
def home():
    user = db.session.query(User).filter_by(id = session.get("id")).first()
    return render_template('index.html', user=user, title="Home")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        user = User(name = name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title="register")

@app.route("/login", methods=['GET', 'POST'])
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
@app.route('/logout')
def logout():
    session["id"] = None
    return redirect(url_for("login"))





with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
