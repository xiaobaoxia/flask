# coding=utf-8
from flask import request, jsonify, g, current_app
import datetime
from iHome.api_1_0 import api
from iHome.utils.common import login_required
from iHome.utils.response_code import RET
from iHome.models import House, Order
from iHome import db


@api.route('/orders', methods=['POST'])
@login_required
def add_order():
    json_data = request.json
    sd = json_data.get('sd')
    ed = json_data.get('ed')
    house_id = json_data.get('house_id')

    user_id = g.user_id
    if not all([sd, ed, house_id, user_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不全')

    try:
        sd = datetime.datetime.strptime(sd, '%Y-%m-%d')
        ed = datetime.datetime.strptime(ed, '%Y-%m-%d')
        assert ed > sd, Exception('结束时间要大于起始时间')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')

    if not house:
        return jsonify(errno=RET.NODATA, errmsg='房屋不存在')

    if house.user_id == user_id:
        return jsonify(errno=RET.ROLEERR, errmsg='房东不能预订房屋')

    try:
        order = Order.query.filter(Order.begin_date < ed, Order.end_date > sd, Order.house_id == house_id).first()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')

    if order:
        return jsonify(errno=RET.DATAEXIST, errmsg='该房屋已被预订')

    order = Order()
    order.user_id = user_id
    order.house_id = house_id
    order.begin_date = sd
    order.end_date = ed
    order.days = (ed-sd).days
    order.house_price = house.price
    order.amount = house.price * order.days

    house.order_count += 1
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DATAERR, errmsg='数据保存失败')

    return jsonify(errno=RET.OK, errmsg='ok')


@api.route('/orders')
@login_required
def get_orders():
    user_id = g.user_id
    role = request.args['role']

    try:
        if role == 'custom':
            orders_query = Order.query.filter(Order.user_id == user_id).order_by(Order.create_time.desc()).all()
        elif role == 'landlord':
            house_id_list = [house.id for house in House.query.filter_by(user_id=user_id).all()]
            orders_query = Order.query.filter(Order.house_id.in_(house_id_list)).order_by(Order.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据失败')

    order_dict = []
    for order in orders_query:
        order_dict.append(order.to_dict())

    return jsonify(errno=RET.OK, errmsg='ok', data={'orders': order_dict})


@api.route('/orders', methods=["PUT"])
@login_required
def change_order_status():
    user_id = g.user_id

    order_id = request.json.get('order_id')

    action = request.json.get('action')

    if not all([user_id, order_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        order = Order.query.get(order_id)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')

    if not order:
        return jsonify(errno=RET.NODATA, errmsg='订单不存在')

    if user_id != order.house.user_id:
        return jsonify(errno=RET.ROLEERR, errmsg='权限有误')

    if action not in ['accept', 'reject']:
        return jsonify(errno=RET.PARAMERR, errmsg='参数有误')
    if action == 'accept':
        order.status = 'WAIT_COMMENT'
    elif action == 'reject':
        reason = request.json.get('reason')
        if not reason:
            return jsonify(errno=RET.PARAMERR, errmsg='请填写拒单原因')
        order.status = 'REJECTED'
        order.comment = reason

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据保存失败')

    return jsonify(errno=RET.OK, errmsg='ok', data=order.to_dict())


@api.route('/orders/comment', methods=['PUT'])
@login_required
def order_comment():
    user_id = g.user_id
    order_id = request.json['order_id']
    comment = request.json['comment']

    if not all([user_id, order_id, comment]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        order = Order.query.get(order_id)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')

    if not order:
        return jsonify(errno=RET.NODATA, errmsg='订单不存在')

    order.comment = comment
    order.status = 'COMPLETE'
    try:
        db.session.commit()

    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据保存错误')

    return jsonify(errno=RET.OK, errmsg='ok', data=order.to_dict())