# -*- coding: utf-8 -*-
class Config(object):
    DEBUG = True
    SECRET_KEY = 'generate secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    BUNDLE_ERRORS = True  # flask-restful

    TIMEZONE = 'Asia/Shanghai'

    # config your app_key and app_id
    CRYPTOPAY_APP_ID = ''
    CRYPTOPAY_APP_KEY = ''
    # development url : http://api.staging.cryptopay.icaicloud.com
    # production url : http://api.cryptopay.icaicloud.com
    CRYPTOPAY_BASE_URL = 'http://api.cryptopay.icaicloud.com'


    PRODUCT_NAME = 'dizpay-demo'

