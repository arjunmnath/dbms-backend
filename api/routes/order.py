from flask import request, jsonify
from flask_restful import Resource
from api.models import create_connection
from mysql.connector import Error
from api.routes import api

from flask import request, jsonify
from flask_restful import Resource
from mysql.connector import Error
from api.models import create_connection  # Adjust the import based on your file structure
from api.routes import api

# Resource for managing user orders
class UserOrdersResource(Resource):
    def get(self, user_id):
        """Fetch all orders for a specific user."""
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM orders WHERE userId = %s", (user_id,)
            )
            orders = cursor.fetchall()
            # Format the orders' paymentTime and orderDate if necessary
            for order in orders:
                order['orderDate'] = order['orderDate'].isoformat() if order['orderDate'] else None
                order['paymentTime'] = order['paymentTime'].isoformat() if order['paymentTime'] else None
                order['totalAmount'] = float(order['totalAmount'])
            return jsonify(orders), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()

    def post(self, user_id):
        """Create a new order for a specific user."""
        data = request.get_json()
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO orders (userId, orderDate, orderStatus, paymentTime, paymentStatus, paymentMethod, totalAmount, transactionId, productId) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (user_id, data['orderDate'], data['orderStatus'], data.get('paymentTime'), 
                 data['paymentStatus'], data['paymentMethod'], data['totalAmount'], 
                 data['transactionId'], data['productId'])
            )
            connection.commit()
            return jsonify({'message': 'Order created successfully'}), 201
        except Error as e:
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()
            connection.close()

    def put(self, user_id, order_id):
        """Update an existing order for a specific user."""
        data = request.get_json()
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE orders 
                SET orderStatus = %s, paymentTime = %s, paymentStatus = %s, 
                    paymentMethod = %s, totalAmount = %s, transactionId = %s, productId = %s 
                WHERE userId = %s AND orderId = %s
                """,
                (data.get('orderStatus'), data.get('paymentTime'), data.get('paymentStatus'),
                 data.get('paymentMethod'), data.get('totalAmount'), data.get('transactionId'),
                 user_id, order_id)
            )
            connection.commit()
            if cursor.rowcount == 0:
                return {'error': 'Order not found'}, 404
            
            return jsonify({'message': 'Order updated successfully'}), 200
        except Error as e:
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()
            connection.close()

    def delete(self, user_id, order_id):
        """Delete an order for a specific user."""
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM orders WHERE userId = %s AND orderId = %s", (user_id, order_id)
            )
            connection.commit()
            if cursor.rowcount == 0:
                return {'error': 'Order not found'}, 404
            
            return jsonify({'message': 'Order deleted successfully'}), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()

# Register the resource with the API
api.add_resource(UserOrdersResource, '/api/v2/users/<int:user_id>/orders', '/api/v2/users/<int:user_id>/orders/<int:order_id>')
