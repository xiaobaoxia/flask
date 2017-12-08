# coding=utf-8
from flask import request, jsonify, current_app, session
from iHome.models import User
from iHome.utils.response_code import RET
from iHome import redis_store, db
from iHome.api_1_0 import api


@api.route('/user', methods=['POST'])
def register():
    '''
    1. 获取参数
    2. 校验参数
    3. 对比验证码, 密码是否合法
    4. 保存用户
    5. 保存用户登录状态返回数据
    :return:
    '''
    data_dict = request.json
    mobile = data_dict['mobile']
    phonecode = data_dict['phonecode']
    password = data_dict['password']
    password2 = data_dict['password2']
    if not all([mobile, phonecode, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg='数据不完整')

    try:
        real_phonecode = redis_store.get('SMS_' + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg='短信验证码查询错误')

    if not real_phonecode:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码过期')

    if real_phonecode != phonecode:
        return jsonify(error=RET.DBERR, errmsg='短信验证码错误')

    if password != password:
        return jsonify(errno=RET.DATAERR, errmsg='两次密码不相等')

    user = User()
    user.name = mobile
    user.mobile = mobile
    user.password = password

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据保存错误')

    # 保存登录状态
    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile

    return jsonify(errno=RET.OK, errmsg='注册成功')


@api.route('/session', methods=['POST'])
def login():
    '''
    1. 获取参数 校验
    2. 判断用户是否存在
    3. 判断用户密码是否正确
    4. 保存用户登录状态
    5. 返回结果
    :return:
    '''
    data_dict = request.json
    mobile = data_dict['mobile']
    password = data_dict['password']

    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据错误')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg='密码错误')

    session['user_id'] = user.id
    session["name"] = user.name
    session["mobile"] = user.mobile

    return jsonify(errno=RET.OK, errmsg='登陆成功')


