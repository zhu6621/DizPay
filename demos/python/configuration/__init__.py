# -*- coding: utf-8 -*-
class Config(object):
    DEBUG = True
    SECRET_KEY = '\n\xb5\x11\xfa\x93*\xd7p[\xe6\xa2\xb7\xa0@\xec\x10\x9f\xee\xd8\xc9\xc0\x94\x80\xd9'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    BUNDLE_ERRORS = True  # flask-restful

    TIMEZONE = 'America/New_York'

    # config your app_key and app_id
    CRYPTOPAY_APP_ID = ''
    CRYPTOPAY_APP_KEY = ''
    # development url : http://api.staging.cryptopay.icaicloud.com
    # production url : http://api.cryptopay.icaicloud.com
    CRYPTOPAY_BASE_URL = 'http://api.staging.cryptopay.icaicloud.com'

    FIAT_CURRENCY = 'USDB'

    PRODUCT_NAME = 'dizpay-demo'

