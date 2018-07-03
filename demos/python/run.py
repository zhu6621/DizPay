# -*- coding: utf-8 -*-
from flask import request
from app import create_app
from app.api import init_api

app = create_app()
init_api(app)


@app.after_request
def update_response(response):
    response.headers['Access-Control-Allow-Origin'] = request.environ.get('HTTP_ORIGIN')
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept, Range, Origin, X-Requested-With'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, HEAD'
    response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == '__main__':
    app.run()
