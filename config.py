# coding=utf-8
import redis


class Config(object):
    SECRET_KEY = 'Alj2oWAjhqKiOIM9jPOJkSR4KNea8igzZde7oGdPuoGRuIaQ3a12wekqJqG2FP5l'
    # MySQL配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config = {
    'DevelopmentConfig': DevelopmentConfig,
    'ProductionConfig': ProductionConfig
}