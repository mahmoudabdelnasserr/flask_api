from flask_jwt_extended import JWTManager

from db import db
from flask_restful import Api
from flask import Flask
import os
from flask_uploads import configure_uploads
from libs.image_helper import IMAGE_SET
from resources.users import UserRegister, Users, UsersList, UserLogin, ResetPassword
from resources.about_us import About_us
from resources.terms_and_conditions import terms_and_conditions
from resources.contact_us import contact_us

app = Flask(__name__)
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neighbor:neighbor@localhost/neighbor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
app.config['UPLOADED_IMAGES_DEST'] = os.path.dirname(os.path.abspath(__file__)) + '/static/images'
app.config['AUDIO_FOLDER'] = os.path.dirname(os.path.abspath(__file__)) + '/static/audios'
app.config['VIDEO_FOLDER'] = os.path.dirname(os.path.abspath(__file__)) + '/static/videos'
app.config['DOCUMENT_FOLDER'] = os.path.dirname(os.path.abspath(__file__)) + '/static/documents'

app.config['patch_request_class'] = (app, 10 * 1024 * 1024)  # restrict max upload image size to 10MB
configure_uploads(app, IMAGE_SET)
app.secret_key = 'jose'
api = Api(app)

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Users, '/user/<int:user_id>')
api.add_resource(UsersList, '/users')
api.add_resource(ResetPassword, '/reset_password/<int:user_id>')
api.add_resource(About_us, '/aboutus')
api.add_resource(terms_and_conditions, '/terms')
api.add_resource(contact_us, '/contact')



if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
