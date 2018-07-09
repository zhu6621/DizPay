import decimal
import requests
import uuid
from flask import g, current_app
from flask_restful import Resource, marshal_with, fields, abort
from cryptopay_sdk import ApiError as CryptoPayApiError
from app.api import login_required, CustomRequestParser, pagination_query, restful_api, cryptopay_api
from app.api.user import user_fields
from app.model import DecimalToString, UtcDatetime2Timestamp, db
from app.model.wallet import Wallet, TransferOrder
from app.model.user import User

member_wallet_fields = {
    'id': fields.String,
    'currency_id': fields.String,
    'address': fields.String,
    'balance': DecimalToString,
    'address_qr_code': fields.String
}

member_wallet_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(member_wallet_fields))
}


class MemberWalletListApi(Resource):
    decorators = [login_required]

    @marshal_with(member_wallet_list_fields)
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('currency', type=str, location='args')

        parsed_args = parser.parse_args()

        wallet = Wallet.query.filter(Wallet.user_id == g.current_user.id,
                                     Wallet.currency_id != 'USDT',
                                     Wallet.currency_id != 'DASH',
                                     Wallet.currency_id != 'BTG',
                                     Wallet.currency_id != 'BCH', )

        if parsed_args['currency']:
            wallet = wallet.filter_by(currency_id=parsed_args['currency'])

        wallet_list = pagination_query(parsed_args['per_page'], parsed_args['page'], wallet)
        objects = []
        sort_currency = ['BTC', 'ETH', 'LTC']
        for currency in sort_currency:
            for item in wallet_list['objects']:
                if item.currency_id == currency:
                    objects.append(item)
                    break

        wallet_list['objects'] = objects
        Wallet.query_wallet(wallet_list['objects'])

        return wallet_list


restful_api.add_resource(MemberWalletListApi, '/api/wallet')

member_transfer_order_fields = {
    'number': fields.String,
    'currency_id': fields.String,
    'to_address': fields.String,
    'amount': DecimalToString,
    'fee': DecimalToString,
    'status': fields.Integer,
    'type': fields.Integer,
    'message': fields.String,
    'user': fields.Nested(user_fields),
    'to_user': fields.Nested(user_fields),
    'created_at': UtcDatetime2Timestamp
}

member_transfer_order_list_fields = {
    'total_pages': fields.Integer,
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total_count': fields.Integer,
    'objects': fields.List(fields.Nested(member_transfer_order_fields))
}


class MemberTransferOrderApi(Resource):
    decorators = [login_required]

    @marshal_with(member_transfer_order_list_fields)
    def get(self):
        parser = CustomRequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('currency', type=str, location='args')
        parser.add_argument('status', type=int, location='args')
        parser.add_argument('type', type=int, location='args')
        parsed_args = parser.parse_args()

        q = TransferOrder.query.filter(db.or_(TransferOrder.user_id == g.current_user.id,
                                              TransferOrder.to_user_id == g.current_user.id))

        if parsed_args['currency']:
            q = q.filter(TransferOrder.currency_id == parsed_args['currency'])
        if parsed_args['status'] is not None:
            q = q.filter(TransferOrder.status.op('&')(parsed_args['status']) != 0)
        if parsed_args['type']:
            q = q.filter(TransferOrder.type == parsed_args['type'])

            q = q.order_by(TransferOrder.created_at.desc())
        return pagination_query(parsed_args['per_page'], parsed_args['page'], q)

    @marshal_with(member_transfer_order_fields)
    def post(self):
        parser = CustomRequestParser()
        parser.add_argument('currency', type=str, required=True, nullable=False, location='json')
        parser.add_argument('amount', type=decimal.Decimal, required=True, nullable=False, location='json')
        parser.add_argument('fee', type=decimal.Decimal, nullable=False, location='json')
        parser.add_argument('message', type=unicode, location='json')
        parsed_args = parser.parse_args()

        wallet = Wallet.query.filter_by(user_id=g.current_user.id,
                                        currency_id=parsed_args['currency']).first()

        if wallet is None:
            abort(400, code=1001, message={'currency': 'currency does not exist'})

        if parsed_args["currency"] == "BTC":
            if parsed_args['amount'] <= decimal.Decimal("0.000001"):
                abort(400, code=1003, message={'amount': 'amount <= 0.00001'})
        elif parsed_args["currency"] == "ETH":
            if parsed_args['amount'] <= 0.00001:
                abort(400, code=1003, message={'amount': 'amount <= 0.0001'})

        order = TransferOrder(user_id=g.current_user.id,
                              currency_id=parsed_args['currency'],
                              amount=parsed_args['amount'],
                              fee=parsed_args['fee'],
                              message=parsed_args['message'])

        db.session.add(order)
        db.session.flush()

        TransferOrder.create_transaction_order(order.number,
                                               wallet.address,
                                               order.amount,
                                               order.fee,
                                               type=order.type)

        TransferOrder.pay_order(order.number)

        order.status = 2
        db.session.commit()
        return order


restful_api.add_resource(MemberTransferOrderApi, '/api/transfer_order')


class MemberTransferOrderDetailApi(Resource):
    decorators = [login_required]

    @marshal_with(member_transfer_order_fields)
    def get(self, order_number):
        order = TransferOrder.query.filter(TransferOrder.number == order_number,
                                           db.or_(TransferOrder.user_id == g.current_user.id,
                                                  TransferOrder.to_user_id == g.current_user.id)).first()
        if order is None:
            abort(400, code=1001, message={'order_number': 'order does not exist'})
        return order


restful_api.add_resource(MemberTransferOrderDetailApi, '/api/transfer_order/<string:order_number>')


class CurrencyConvertApi(Resource):
    def get(self):
        currency_dic = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'LTC': 'litecoin',
        }
        result = []
        for (key, value) in currency_dic.items():
            r = requests.get('https://api.coinmarketcap.com/v1/ticker/{}/'.format(value),
                             timeout=(19, 19))
            result.append(r.json()[0])
        return result


restful_api.add_resource(CurrencyConvertApi, '/api/currency_convert')


class ChargeOrderApi(Resource):
    def post(self):
        parser = CustomRequestParser()
        parser.add_argument('amount', type=str, required=True, nullable=False, location='json')
        parsed_args = parser.parse_args()
        api = cryptopay_api()
        url = '{}/member/create_charge_order'.format(current_app.config['CRYPTOPAY_BASE_URL'])
        currency_overt = CurrencyConvertApi()
        current_covert = currency_overt.get()
        for item in current_covert:
            if item['symbol'] == 'BTC':
                BTC = float(parsed_args['amount']) / float(item['price_usd'])
            elif item['symbol'] == 'ETH':
                ETH = float(parsed_args['amount']) / float(item['price_usd'])
        payments = 'BTC={};ETH={}'.format(BTC, ETH)
        data = {
            'number': str(uuid.uuid4()),
            'amount': parsed_args['amount'],
            'payments': payments,
            'extra': ''
        }
        try:
            result = api.post(url, data)
        except CryptoPayApiError as e:
            abort(e.http_status_code, code=e.code, message=e.message)
        result['currency_address_qr_code'] = current_app.config['CRYPTOPAY_BASE_URL'] + '/currency_address_qr_code'
        return result


restful_api.add_resource(ChargeOrderApi, '/api/create_charge_order')

