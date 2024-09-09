from flask import request, jsonify
from models import db, Order
from sqlalchemy.exc import IntegrityError
from . import appbp

# Get orders for a user
@appbp.route('/api/users/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    try:
        orders = Order.query.filter_by(userId=user_id).all()
        orders_list = [
            {
                'orderId': o.orderId,
                'orderDate': o.orderDate.isoformat(),
                'orderStatus': o.orderStatus,
                'paymentTime': o.paymentTime.isoformat() if o.paymentTime else None,
                'paymentStatus': o.paymentStatus,
                'paymentMethod': o.paymentMethod,
                'totalAmount': float(o.totalAmount),
                'transactionId': o.transactionId,
                'productId': o.productId
            } for o in orders
        ]
        return jsonify(orders_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
