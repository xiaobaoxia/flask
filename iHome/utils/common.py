# coding=utf-8
'''自定义转换器'''
from werkzeug.routing import BaseConverter
import functools
from flask import session, jsonify, g
from iHome.utils.response_code import RET


class RegexConverter(BaseConverter):

    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


def login_required(f):
    @functools.wraps(f)
    def warpper(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
        g.user_id = user_id
        return f(*args, **kwargs)
    return warpper