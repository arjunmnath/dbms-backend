from flask import request, jsonify
from flask_restful import Resource
from api.models import create_connection
from mysql.connector import Error
from api.routes import api

# Resource for managing messages
class MessagesResource(Resource):
    def post(self):
        """Send a new message."""
        data = request.get_json()
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO messages (sentTime, readTime, messageContent, productId, sellerId, receiverId) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (data['sentTime'], data.get('readTime'), data['messageContent'], 
                 data.get('productId'), data['sellerId'], data['receiverId'])
            )
            connection.commit()
            return jsonify({'message': 'Message sent successfully'}), 201
        except Error as e:
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()
            connection.close()

class UserMessagesResource(Resource):
    def get(self, user_id):
        """Fetch all messages for a specific user (either sent or received)."""
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT * FROM messages 
                WHERE sellerId = %s OR receiverId = %s
                """,
                (user_id, user_id)
            )
            messages = cursor.fetchall()
            return jsonify(messages), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()

class MessageResource(Resource):
    def get(self, message_id):
        """Fetch a single message by its ID."""
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM messages WHERE messageId = %s", (message_id,)
            )
            message = cursor.fetchone()
            if not message:
                return {'error': 'Message not found'}, 404
            
            return jsonify(message), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()

    def put(self, message_id):
        """Update a message's read time or content."""
        data = request.get_json()
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE messages 
                SET readTime = %s, messageContent = %s 
                WHERE messageId = %s
                """,
                (data.get('readTime'), data.get('messageContent'), message_id)
            )
            connection.commit()
            if cursor.rowcount == 0:
                return {'error': 'Message not found'}, 404
            
            return jsonify({'message': 'Message updated successfully'}), 200
        except Error as e:
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()
            connection.close()

    def delete(self, message_id):
        """Delete a message by its ID."""
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM messages WHERE messageId = %s", (message_id,))
            connection.commit()
            if cursor.rowcount == 0:
                return {'error': 'Message not found'}, 404
            
            return jsonify({'message': 'Message deleted successfully'}), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()

# Register the resources with the API
api.add_resource(MessagesResource, '/api/v2/messages')
api.add_resource(UserMessagesResource, '/api/v2/users/<int:user_id>/messages')
api.add_resource(MessageResource, '/api/v2/messages/<int:message_id>')