# -*- coding: utf-8 -*-
import uuid
import datetime
from flask import g
from flask_restful import Resource, fields, marshal_with, abort
from werkzeug.http import dump_cookie
from app.api import restful_api, CustomRequestParser, login_required
from app.model import db
from app.model.user import User
from app.model.wallet import Wallet

user_fields = {
    'id': fields.String,
    'mobile': fields.String,
    'token': fields.String,
}


class UserApi(Resource):
    decorators = [login_required]

    @marshal_with(user_fields)
    def get(self):
        user = g.current_user
        return user


restful_api.add_resource(UserApi, '/api/user')


# password login
class SmsPinCodedLoginApi(Resource):
    @marshal_with(user_fields)
    def post(self):
        parser = CustomRequestParser()
        parser.add_argument('mobile', type=str, required=True, nullable=False, location='json')
        parser.add_argument('password', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()

        user = User.query.filter(User.mobile == parsed_args['mobile']).first()
        if user is None:
            user = User(id=str(uuid.uuid4()),
                        mobile=parsed_args['mobile'])
            user.set_password(parsed_args['password'])
            user.generate_auth_token()
            db.session.add(user)
            db.session.commit()
            Wallet.generate_wallet(user.id, None)
        else:
            if not user.verify_password(parsed_args['password']):
                abort(400, code=1002, message={'password': 'password does not match'})
            user.generate_auth_token()
            user.save()

        cookie = dump_cookie(key='token', value=user.token, max_age=datetime.timedelta(days=1000))
        return user, {'Set-Cookie': cookie}


restful_api.add_resource(SmsPinCodedLoginApi, '/api/password_login')


# logout
class LogoutApi(Resource):
    decorators = [login_required]

    def post(self):
        g.current_user.generate_auth_token()
        db.session.commit()
        return {}, {'Set-Cookie': dump_cookie('token', max_age=0)}


restful_api.add_resource(LogoutApi, '/api/log_out')
