# coding=utf-8
from flask import request, abort, jsonify, current_app, make_response
from iHome.utils.captcha.captcha import captcha
from iHome import redis_store
from iHome import constants
from iHome.utils.response_code import RET
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