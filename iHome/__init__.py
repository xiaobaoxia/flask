# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import redis
from config import config
import api_1_0
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


db = SQLAlchemy()
csrf = CSRFProtect()
redis_store = None


def create_app(config_name):
    app = Flask(__name__)
    app.register_blueprint(api_1_0.api, url_prefix='/api/v1.0')
    app.config.from_object(config[config_name])
    Session(app)
    db.init_app(app)
    csrf.init_app(app)
    global redis_store
    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)
    return app