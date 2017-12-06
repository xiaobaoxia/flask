# coding=utf-8
'''自定义转换器'''
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):

    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]

