# -*- coding: utf-8 -*-
from flask import current_app
from flask_restful import abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash
from app.model import db, UuidBaseModel


class User(UuidBaseModel):
    mobile = db.Column(db.String(16), unique=True)  # 用户手机号
    token = db.Column(db.String(256))  # 访问令牌
    password = db.Column(db.String(256), nullable=False)  # 密码

    def generate_auth_token(self, expiration=31 * 24 * 60 * 60, parameter=None):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        data = {'id': self.id}
        if parameter:
            data = dict(data.items() + parameter.items())
        self.token = s.dumps(data)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def verify_auth_token(cls, token):
        # if not token:
        #     return None
        if not token:
            abort(401, code=1001, message={'token': 'token does not exist'})
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None, None  # valid token, but expired
        except BadSignature:
            return None, None  # invalid token
        user = cls.query.get(data['id'])
        if user and user.token == token:
            return user, data
        return None, None
