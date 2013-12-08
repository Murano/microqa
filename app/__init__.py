from flask import Flask

from app.config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

from app import views
