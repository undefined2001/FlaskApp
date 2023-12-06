from flask import Flask, render_template, request, redirect, url_for, session
from models import Pet, User, db
from blueprints import admin_bp, pet_bp, user_bp
import os

app = Flask(__name__)

#!Configs for the Flask App
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://mysql:root@localhost:3306/flaskapp"
app.config["SECRET_KEY"] = "Asraful"
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'media')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

#*Registering Bluprints
app.register_blueprint(admin_bp)
app.register_blueprint(pet_bp)
app.register_blueprint(user_bp)

db.init_app(app)

#*Section For Context Preprocessor
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
    
@app.context_processor
def admin_user_name():
    user = db.session.query(User).filter_by(id = session.get("id")).first()
    if user and user.role == "admin":
        return {'admin_user_name':user.name}
    else:
        return {'admin_user_name':"Not Found"}
    
#*End of Contex Preprocessor Section

@app.route("/")
def home():
    pets = db.session.query(Pet).all()
    return render_template('index.html', pets=pets, title="Home")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
