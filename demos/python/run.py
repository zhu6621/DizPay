# -*- coding: utf-8 -*-
from flask import session, request, redirect, jsonify
from app import create_app
from app.api import init_api

app = create_app()
init_api(app)


def is_ajax_request():
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


if __name__ == '__main__':
    app.run()
