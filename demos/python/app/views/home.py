from flask import render_template, Blueprint, jsonify
from app.views import Api

home = Blueprint('home', __name__)


@home.route('/login')
def login():
    return render_template('login.html')


@home.route('/wallet')
def wallet():
    return render_template('wallet.html')


@home.route('/ajax/user')
def ajax_user():
    return jsonify(Api.get('/api/user'))
