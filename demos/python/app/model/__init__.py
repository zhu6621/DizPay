# -*- coding: utf-8 -*-
import calendar
import datetime
import time
import uuid
import random
import decimal
from flask_sqlalchemy import SQLAlchemy
from flask_restful import fields

db = SQLAlchemy(session_options={"autoflush": False})


def now_timestamp():
    return int(time.time())


def timestamp_to_utc_datetime(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp)


def utc_datetime_to_timestamp(utc_datetime):
    return calendar.timegm(utc_datetime.timetuple())


def generate_timestamp_id():
    return str(int(time.time()) * 1000000 + random.randint(100000, 999999))


class DecimalToString(fields.Raw):
    def format(self, value):
        return '{0:.8f}'.format(decimal.Decimal(value))


class UtcDatetime2Timestamp(fields.Raw):
    def __init__(self, **kwargs):
        super(UtcDatetime2Timestamp, self).__init__(default=0, **kwargs)

    def format(self, value):
        return utc_datetime_to_timestamp(value)


class UuidBaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), default=uuid.uuid4, primary_key=True)
    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow,
                           nullable=False)
    updated_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow,
                           nullable=False)

    @property
    def created_timestamp(self):
        return utc_datetime_to_timestamp(self.created_at)

    @property
    def updated_timestamp(self):
        return utc_datetime_to_timestamp(self.updated_at)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class AutoIncrementBaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow,
                           nullable=False)
    updated_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow,
                           nullable=False)

    @property
    def created_timestamp(self):
        return utc_datetime_to_timestamp(self.created_at)

    @property
    def updated_timestamp(self):
        return utc_datetime_to_timestamp(self.updated_at)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow,
                           nullable=False)
    updated_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow,
                           nullable=False)


class UuidBase(BaseModel):
    __abstract__ = True

    id = db.Column(db.String(36), default=uuid.uuid4, primary_key=True)


class AutoIncrementBase(BaseModel):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class OrderBase(AutoIncrementBase):
    __abstract__ = True

    number = db.Column(db.String(16), default=generate_timestamp_id, unique=True, nullable=False)
