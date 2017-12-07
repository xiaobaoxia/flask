# coding=utf-8
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