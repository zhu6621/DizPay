# -*- coding: utf-8 -*-
import json
from app.model import db, UuidBase, OrderBase
from app.model.user import User
from app.api import cryptopay_api
from flask import current_app, g
from cryptopay_sdk import ApiError as CryptoPayApiError
from flask_restful import abort


class Wallet(UuidBase):
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    currency_id = db.Column(db.String(50), nullable=False)  # 货币代码
    address = db.Column(db.String(100), unique=True, nullable=False)  # 区块链币地址
    address_qr_code = db.Column(db.String(512))  # 地址二维码 URL

    __table_args__ = (db.UniqueConstraint('user_id', 'currency_id'),)

    # relationship
    user = db.relationship(User)

    @staticmethod
    def generate_wallet(user_id, currency_list):
        api = cryptopay_api()
        url = '{}/member/create_wallet'.format(current_app.config['CRYPTOPAY_BASE_URL'])
        data = {
            'currency_list': currency_list
        }
        try:
            wallet_list = api.post(url, data)
            for w in wallet_list['objects']:
                address_qr_code = '%s/currency_address_qr_code/%s' % (current_app.config['CRYPTOPAY_BASE_URL'], w['address'])
                wallet = Wallet(user_id=user_id,
                                currency_id=w['currency_id'],
                                address=w['address'],
                                address_qr_code=address_qr_code)
                db.session.add(wallet)
            db.session.commit()
        except CryptoPayApiError as e:
            abort(e.http_status_code, code=e.code, message=e.message)

    @staticmethod
    def query_wallet(wallet_list):
        address_list = []
        for wallet in wallet_list:
            address_list.append(wallet.address)

        api = cryptopay_api()
        url = '{}/member/query_wallet'.format(current_app.config['CRYPTOPAY_BASE_URL'])
        data = {
            'address_list': ','.join(address_list)
        }
        try:
            address_balance_dict = {}
            query_wallet_list = api.post(url, data)
            for query_wallet in query_wallet_list['objects']:
                address_balance_dict[query_wallet['address']] = query_wallet['balance']
            for wallet in wallet_list:
                wallet.balance = address_balance_dict.get(wallet.address, '0')
        except CryptoPayApiError as e:
            abort(e.http_status_code, code=e.code, message=e.message)


class TransferOrder(OrderBase):
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.SmallInteger, default=2)  # 1 内部转账  2 商家付款
    currency_id = db.Column(db.String(50), nullable=False)  # 货币代码
    amount = db.Column(db.Numeric(24, 8), nullable=False)  # 金额
    fee = db.Column(db.Numeric(24, 8), nullable=False, default=0)  # 手续费
    status = db.Column(db.SmallInteger, default=1, nullable=False)  # 1 确认中  2 成功  4 失败
    message = db.Column(db.String(140))

    user = db.relationship('User', foreign_keys=[user_id], remote_side="User.id")

    @staticmethod
    def create_transaction_order(order_number, address, amount, fee, type=2):
        api = cryptopay_api()
        url = '{}/member/create_transaction_order'.format(current_app.config['CRYPTOPAY_BASE_URL'])
        data = {
            'number': order_number,
            'address': address,
            'amount': str(amount),
            'fee': str(fee),
            'extra': json.dumps({'type': type})
        }
        try:
            return api.post(url, data)
        except CryptoPayApiError as e:
            abort(e.http_status_code, code=e.code, message=e.message)

    @staticmethod
    def pay_order(order_number):
        api = cryptopay_api()
        url = '{}/member/pay_order'.format(current_app.config['CRYPTOPAY_BASE_URL'])
        data = {
            'number': order_number
        }
        try:
            return api.post(url, data)
        except CryptoPayApiError as e:
            abort(e.http_status_code, code=e.code, message=e.message)
