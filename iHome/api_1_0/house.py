# coding=utf-8
from flask import current_app, jsonify
from iHome import db, redis_store
from iHome.utils.response_code import RET
from iHome import constants
from iHome.api_1_0 import api
from iHome.models import Area


@api.route('/areas')
def get_areas():
    try:
        areas_dict = redis_store.get('areas_dict')
    except Exception as e:
        current_app.logger.error(e)
    if areas_dict:
        return jsonify(errno=RET.OK, errmsg='ok', data=eval(areas_dict))
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    areas_dict = []
    for area in areas:
        areas_dict.append(area.to_dict())
    try:
        redis_store.set('areas', areas_dict, constants.AREA_INFO_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)

    return jsonify(errno=RET.OK, errmsg='OK', data=areas_dict)


@api.route('/')