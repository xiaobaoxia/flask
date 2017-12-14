# coding=utf-8
from flask import Blueprint, make_response, request
from flask_wtf.csrf import generate_csrf

static_api = Blueprint('static', __name__, static_folder='static')


@static_api.route('/<re(".*"):file_name>')
def static_html(file_name):
    if not file_name:
        file_name = 'index.html'
    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name

    response = make_response(static_api.send_static_file(file_name))
    response.set_cookie('csrf_token', generate_csrf())

    return response




