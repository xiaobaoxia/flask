# coding=utf-8

from iHome.api_1_0 import api
from flask import request, g, current_app, jsonify, session
from iHome.models import User
from iHome.utils.common import login_required
from iHome.utils.response_code import RET
from iHome.utils.image_storage import storage_image
from iHome import db
from iHome import constants


# 个人信息页
@api.route('/user')
@login_required
def get_user_info():
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    return jsonify(errno=RET.OK, errmsg='OK', data=user.to_dict())


# 修改用户名
@api.route('/user/name', methods=['POST'])
@login_required
def set_user_name():
    user_name = request.json['user_name']
    if not user_name:
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')
    user.name = user_name
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存失败')

    session['name'] = user_name
    return jsonify(errno=RET.OK, errmsg='OK')


# 修改头像
@api.route('/user/avatar', methods=['POST'])
@login_required
def set_user_avatar():
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')
    # 获取图片
    try:
        image = request.files['avatar'].read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    # 上传图片
    try:
        url = storage_image(image)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传图片失败')

    user.avatar_url = url

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='用户数据保存失败')

    return jsonify(errno=RET.OK, errmsg='OK', data={'avatar_url': constants.QINIU_DOMIN_PREFIX + url})