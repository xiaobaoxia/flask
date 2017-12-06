# coding=utf-8
from flask import Blueprint

static_api = Blueprint('static', __name__, static_folder='static')


@static_api.route('/<re(".*"):file_name>')
def static_html(file_name):
    if not file_name:
        file_name = 'index.html'
    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name

    return static_api.send_static_file(file_name)



