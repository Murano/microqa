from flask import Flask
from flask.ext.login import LoginManager
from model import User

from app.config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.objects(id=userid).first()

from app import views
