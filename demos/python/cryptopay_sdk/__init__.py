# -*- coding: utf-8 -*-
import hashlib
import requests


class ApiError(Exception):
    def __init__(self, http_status_code, code, message):
        self.http_status_code = http_status_code
        self.code = code
        self.message = message


class Api(object):
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def post(self, url, data):
        data['app_id'] = self.app_id
        data['app_key'] = self.app_key
        items = data.items()
        kv_pair_list = []
        for k, v in items:
            kv_pair_list.append('{}={}'.format(k, v.encode('utf-8') if hasattr(v, 'encode') else v))
        kv_pair_list.sort()
        signature = hashlib.md5('&'.join(kv_pair_list)).hexdigest()
        data.pop('app_key')
        data['signature'] = signature
        r = requests.post(url, json=data, timeout=5)
        if r.status_code == requests.codes.ok:
            if r.encoding is None or r.encoding == 'ISO-8859-1':
                r.encoding = 'UTF-8'
            return r.json()
        elif r.status_code == 400:
            error_data = r.json()
            raise ApiError(r.status_code, error_data['code'], error_data['message'])
        else:
            raise ApiError(r.status_code, -1, {})
