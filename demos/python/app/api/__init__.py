# -*- coding: utf-8 -*-
import math
from flask import current_app, g, request, redirect, url_for
from flask_restful import Api, reqparse, Resource, abort
from werkzeug import exceptions
from functools import wraps

restful_api = Api()


class HomeApi(Resource):
    def get(self):
        return {'product_name': current_app.config['PRODUCT_NAME']}


restful_api.add_resource(HomeApi, '/api/')


def init_api(app):
    from app.api import user
    from app.api import wallet

    restful_api.init_app(app)


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        from app.model.user import User
        token = request.args.get('token')
        if not token:
            token = request.cookies.get('token')
        g.current_user, g.token_parameter = User.verify_auth_token(token)
        if g.current_user is None:
            abort(401)
        return func(*args, **kwargs)

    return decorated_view


class CustomRequestParser(reqparse.RequestParser):
    def parse_args(self, req=None, strict=False):
        """Parse all arguments from the provided request and return the results
        as a Namespace

        :param strict: if req includes args not in parser, throw 400 BadRequest exception
        """
        if req is None:
            req = request

        namespace = self.namespace_class()

        # A record of arguments not yet parsed; as each is found
        # among self.args, it will be popped out
        req.unparsed_arguments = dict(self.argument_class('').source(req)) if strict else {}
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                namespace[arg.dest or arg.name] = value
        if errors:
            abort(400, code=1000, message=errors)

        if strict and req.unparsed_arguments:
            raise exceptions.BadRequest('Unknown arguments: %s'
                                        % ', '.join(req.unparsed_arguments.keys()))

        return namespace


def pagination_calc_page(per_page, page, count):
    if per_page <= 0:
        abort(400, code=1000, message={'per_page': 'per_page must greater than 0'})
    record_count = count
    if record_count == 0:
        record_count = 1
    total_pages = int(math.ceil(record_count / float(per_page)))
    if page <= 0:
        page = total_pages
    return page, total_pages


def pagination_query(per_page, page, query):
    """
    转换为分页结果
    :param per_page: per page count
    :param page: page index
    :param query: query
    :return:
    """
    count = query.count()
    page, total_pages = pagination_calc_page(per_page, page, count)
    pagination = query.paginate(page, per_page, False)
    return {
        'total_pages': total_pages,
        'page': page,
        'per_page': per_page,
        'total_count': count,
        'objects': pagination.items
    }


def cryptopay_api():
    from cryptopay_sdk import Api as CryptoPayApi
    return CryptoPayApi(current_app.config['CRYPTOPAY_APP_ID'],
                        current_app.config['CRYPTOPAY_APP_KEY'])
