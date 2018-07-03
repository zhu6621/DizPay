# -*- coding: utf-8 -*-
class Config(object):
    DEBUG = True
    SECRET_KEY = '\xd4{t0G\xfb\x18okZ\xd9\xa9\x99\x13\x01\x8c\t|5\x92*\xb9\x01\xb1\xc7\xbf\x12\xde\xad\xe3\xe1\xf0'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    BUNDLE_ERRORS = True  # flask-restful

    TIMEZONE = 'Asia/Shanghai'

    # config your app_key and app_id
    CRYPTOPAY_APP_ID = ''
    CRYPTOPAY_APP_KEY = ''
    # development url : http://api.staging.cryptopay.icaicloud.com
    # production url : http://api.cryptopay.icaicloud.com
    CRYPTOPAY_BASE_URL = 'http://api.staging.cryptopay.icaicloud.com'


    PRODUCT_NAME = 'dizpay-demo'

