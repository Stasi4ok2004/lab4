from flask import Flask
from flask_bcrypt import Bcrypt
from blueprints import api_blueprint
app = Flask(__name__)
bycrypted_app = Bcrypt(app)
app.register_blueprint(api_blueprint)

@app.route('/')
def root():
    return ''