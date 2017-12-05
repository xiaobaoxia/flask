# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import redis
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Config(object):
    SECRET_KEY = 'Alj2oWAjhqKiOIM9jPOJkSR4KNea8igzZde7oGdPuoGRuIaQ3a12wekqJqG2FP5l'
    DEBUG = True
    # MySQL配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.191.138:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis配置
    REDIS_HOST = '192.168.191.138'
    REDIS_PORT = 6379

    # session配置




app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
CSRFProtect(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)


@app.route('/', methods=['POST', 'GET'])
def index():
    redis_store.set('name', 'asd')
    return 'index'

if __name__ == '__main__':
    app.run()
