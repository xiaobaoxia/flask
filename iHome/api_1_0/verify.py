# coding=utf-8
from flask import request, abort, jsonify, current_app, make_response
import json
from iHome.utils.captcha.captcha import captcha
from iHome import redis_store
from iHome import constants
from iHome.utils.response_code import RET
import random
import re
from . import api


@api.route('/imagecode')
def get_image_code():
    '''
    1. 获取传入的验证码id
    2. 生成新的验证码
    3. 删除旧的验证码信息, 保存新的验证码信息
    4. 返回验证码图片
    :return:
    '''

    # 获取新验证码和旧验证码ID
    args = request.args
    cur = args.get('cur')
    pre = args.get('pre')
    if not cur:
        abort(403)
    # 获取验证码图片及内容
    _, text, image = captcha.generate_captcha()

    current_app.logger.debug(text)
    # 保存新验证码内容, 删除旧验证码内容
    try:
        redis_store.set('ImageCode_' + cur, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        redis_store.delete('ImageCode_' + pre)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='验证码保存失败')

    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'

    return response


@api.route('/smscode', methods=['POST'])
def send_sms_code():
    '''
    获取手机号, 图片验证码
    对比图片验证码
    成功后生成短信验证码
    保存验证码, 发送短信   手机号: 短信验证码 redis
    :return:
    '''
    json_data = request.get_data()
    args = json.loads(json_data)

    image_code = args['image_code']
    image_code_id = args['image_code_id']
    mobile = args['mobile']
    # 判断数据是否完整
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    # 判断手机号是否合法
    if not re.match("^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号不正确')
    # 判断图片验证码是否正确
    # 获取真实验证码
    try:
        real_image_code = redis_store.get('ImageCode_'+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据异常')

    # 验证码不存在
    if not real_image_code:
        return jsonify(errno=RET.DATAERR, errmsg='验证码已过期')

    # 验证码不正确
    if real_image_code.lower() != image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg='验证码不正确')

    # 删除图片验证码
    try:
        redis_store.delete('ImageCode_'+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='删除本地验证码错误')

    sms_code = '%06d' % random.randint(100000, 999999)

    # 发送成功
    return jsonify(errno=RET.OK, errmsg='发送成功')