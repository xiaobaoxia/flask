# coding=utf-8
from flask import current_app, jsonify, g, request, session
from iHome import db, redis_store
from iHome.utils.response_code import RET
from iHome.utils.common import login_required
from iHome import constants
from iHome.api_1_0 import api
from iHome.models import Area, House, Facility, HouseImage
from iHome.utils.image_storage import storage_image
from iHome.constants import QINIU_DOMIN_PREFIX


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


@api.route('/house', methods=['POST'])
@login_required
def save_new_house():
    user_id = g.user_id
    json_dict = request.json
    title = json_dict.get('title')
    price = json_dict.get('price')
    address = json_dict.get('address')
    area_id = json_dict.get('area_id')
    room_count = json_dict.get('room_count')
    acreage = json_dict.get('acreage')
    unit = json_dict.get('unit')
    capacity = json_dict.get('capacity')
    beds = json_dict.get('beds')
    deposit = json_dict.get('deposit')
    min_days = json_dict.get('min_days')
    max_days = json_dict.get('max_days')

    if not all([title, price, address, area_id, room_count, acreage,
                unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数有误')

    try:
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数有误')
    house = House()
    house.user_id = user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    facility = json_dict.get('facility')
    if facility:
        house.facilities = Facility.query.filter(Facility.id.in_(facility)).all()

    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据错误')

    return jsonify(errno=RET.OK, errmsg='ok', data={'house_id': house.id})


@api.route('/house/image', methods=['POST'])
@login_required
def save_house_image():
    # 获取房屋id
    house_id = request.form['house_id']
    if not house_id:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 获取房屋图片
    try:
        image = request.files.get('house_image').read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 上传图片
    try:
        url = storage_image(image)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传图片错误')
    # 查询房屋信息
    try:
        house = House.query.get(int(house_id))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    if not house:
        return jsonify(errno=RET.DATAERR, errmsg='房屋信息不存在')

    if house.index_image_url == '':
        house.index_image_url = url

    house_image = HouseImage()

    house_image.house_id = house_id
    house_image.url = url

    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据保存失败')

    return jsonify(errno=RET.OK, errmsg='ok', data={"url": QINIU_DOMIN_PREFIX + url})


@api.route('/house/<int:house_id>')
def get_house_detail(house_id):
    user_id = session.get('user_id', -1)
    # if not user_id:
    #     user_id = -1
    if not house_id:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')

    house_info = house.to_full_dict()

    return jsonify(errno=RET.OK, errmsg='OK', data={'house_info': house_info, 'user_id': user_id})

