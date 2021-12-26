import datetime
import traceback

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

from libs.mailgun import MailGunException
from models.confirmation import ConfirmationModel
from models.users import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    parser.add_argument('phone',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    parser.add_argument('profile_image_url',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_email(data['email']):
            return {"message": "A user with this email already exists"}, 400

        if UserModel.find_by_phone(data['phone']):
            return {"message": "A user with this phone already exists"}, 400

        user = UserModel(**data)
        try:
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            user.send_confirmation_email()
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=expires)
            return {
                        'message': 'you are now registered',
                        'access_token': access_token,
                   }, 201
        except MailGunException as e:
            user.delete_from_db()  # rollback
            return {"message": str(e)}, 500
        except:  # failed to save user to db
            traceback.print_exc()
            user.delete_from_db()  # rollback
            return {"message": "user_error_creating"}, 500



class Users(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=False,
                        help="You can keep PI empty."
                        )

    parser.add_argument('phone',
                        type=str,
                        required=False,
                        help="You can keep PI empty."
                        )

    parser.add_argument('email',
                        type=str,
                        required=False,
                        help="You can keep PI empty."
                        )

    parser.add_argument('profile_image_url',
                        type=str,
                        required=False,
                        help="You can keep PI empty."
                        )


    def get(self, user_id):
        user = UserModel.find_by_userid(user_id)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_by_userid(user_id)
        if user:
            user.delete_from_db()
            return {'message': 'user deleted.'}
        return {'message': 'User not found.'}, 404


    def put(self, user_id):

        data = UserRegister.parser.parse_args()
        # data = BaseUserRegister.parser.parse_args()

        user = UserModel.find_by_userid(user_id)

        if user:
            user.username = data['username']
            user.phone = data['phone']
            user.email = data['email']

        else:
            user = UserModel(user_id, **data)

        user.save_to_db()

        return user.json()

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserLogin.parser.parse_args()

        user = UserModel.find_by_email(data['email'])

        # this is what the `authenticate()` function did in security.py
        if user and safe_str_cmp(user.password, data['password']):
            return {'message': 'you are now logged in'} ,200
        return {"message": "Invalid Credentials!"}, 401

class ResetPassword(Resource):
        parser = reqparse.RequestParser()
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )

        parser.add_argument('confirm_password',
                            type=str,
                            required=True,
                            help="This field cannot be blank."
                            )
        def post(self, user_id):
            user = UserModel.find_by_userid(_id=user_id)
            data = ResetPassword.parser.parse_args()
            if data['password'] != data['confirm_password']:
                return {'message': 'password doesn\'t match'}
            user.password = data['password']
            user.save_to_db()
            return {'message': 'password changed successfully'}

class UsersList(Resource):
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}