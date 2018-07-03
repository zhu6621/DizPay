# -*- coding: utf-8 -*-
import requests
from flask import abort, current_app, jsonify, session


class AppError:
    INVALID_REQUEST = 400

    @staticmethod
    def invalid_request(message):
        return ApiError(AppError.INVALID_REQUEST, message)


class ApiError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def to_json(self):
        return jsonify({'code': self.code, 'message': self.message})


class Api:
    @staticmethod
    def url(resource_path):
        return current_app.config['API'] + resource_path

    @staticmethod
    def handle_response(r, response_type='json'):
        if r.status_code == requests.codes.ok:
            if r.encoding is None or r.encoding == 'ISO-8859-1':
                r.encoding = 'UTF-8'
            if response_type == 'json':
                return r.json()
            return r.content
        elif r.status_code == 401:
            abort(401)
        elif r.status_code == 400:
            data = r.json()
            raise ApiError(data['code'], data['message'])
        else:
            raise ApiError(500, 'internal error')

    @staticmethod
    def get(resource_path, params=None, response_type='json'):
        if session.get('token'):
            params = params or {}
            params['token'] = session.get('token')
        r = requests.get(Api.url(resource_path), params, timeout=(9, 18))
        return Api.handle_response(r, response_type)

    @staticmethod
    def post(resource_path, data, response_type='json'):
        if session.get('token'):
            resource_path += '?token={}'.format(session.get('token'))
        r = requests.post(Api.url(resource_path), json=data, timeout=(9, 18))
        return Api.handle_response(r, response_type)

    @staticmethod
    def put(resource_path, data):
        if session.get('token'):
            resource_path += '?token={}'.format(session.get('token'))
        r = requests.put(Api.url(resource_path), json=data, timeout=(9, 18))
        return Api.handle_response(r)

    @staticmethod
    def delete(resource_path):
        if session.get('token'):
            resource_path += '?token={}'.format(session.get('token'), timeout=(9, 18))
        r = requests.delete(Api.url(resource_path))
        return Api.handle_response(r)

    @staticmethod
    def dict_to_object(data):
        class Wrapper:
            def __init__(self, **entries):
                self.__dict__.update(entries)

        return Wrapper(**data)
