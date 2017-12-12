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
    print sd, ed
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
    print sd, ed

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

    # id = db.Column(db.Integer, primary_key=True)  # 订单编号
    # user_id = db.Column(db.Integer, db.ForeignKey("ih_user_profile.id"), nullable=False)  # 下订单的用户编号
    # house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)  # 预订的房间编号
    # begin_date = db.Column(db.DateTime, nullable=False)  # 预订的起始时间
    # end_date = db.Column(db.DateTime, nullable=False)  # 预订的结束时间
    # days = db.Column(db.Integer, nullable=False)  # 预订的总天数
    # house_price = db.Column(db.Integer, nullable=False)  # 房屋的单价
    # amount = db.Column(db.Integer, nullable=False)  # 订单的总金额
    # status = db.Column(  # 订单的状态
    #     db.Enum(
    #         "WAIT_ACCEPT",  # 待接单,
    #         "WAIT_PAYMENT",  # 待支付
    #         "PAID",  # 已支付
    #         "WAIT_COMMENT",  # 待评价
    #         "COMPLETE",  # 已完成
    #         "CANCELED",  # 已取消
    #         "REJECTED"  # 已拒单
    #     ),
    #     default="WAIT_ACCEPT", index=True)
    # comment = db.Column(db.Text)  # 订单的评论信息或者拒单原因
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