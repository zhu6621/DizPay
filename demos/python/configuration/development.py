# -*- coding: utf-8 -*-
from configuration import Config


class DevelopmentConfig(Config):
    DEV_ENV_DATABASE_URI = 'mysql://root:root@localhost:3306/dizpay_demo?charset=utf8mb4'
    TEST_ENV_DATABASE_URI = 'mysql://root:root@localhost:3306/dizpay_demo?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI = DEV_ENV_DATABASE_URI
