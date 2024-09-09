from flask import request, jsonify
from api.models import db, Messages
from sqlalchemy.exc import IntegrityError
from . import appbp

# Send a message
@appbp.route('/api/messages', methods=['POST']) #working fine
def send_message():
    data = request.get_json()
    try:
        new_message = Messages(
            sentTime=data['sentTime'],
            readTime=data.get('readTime'),
            messageContent=data['messageContent'],
            productId=data.get('productId'),
            sellerId=data['sellerId'],
            receiverId=data['receiverId']
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'message': 'Message sent successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Invalid data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Fetch messages for a user (either sent or received)
@appbp.route('/api/users/<int:user_id>/messages', methods=['GET'])
def get_user_messages(user_id):
    try:
        # Fetch messages where the user is either the sender or receiver
        messages = Messages.query.filter(
            (Messages.sellerId == user_id) | (Messages.receiverId == user_id)
        ).all()
        messages_list = [
            {
                'messageId': m.messageId,
                'sentTime': m.sentTime.isoformat(),
                'readTime': m.readTime.isoformat() if m.readTime else None,
                'messageContent': m.messageContent,
                'productId': m.productId,
                'sellerId': m.sellerId,
                'receiverId': m.receiverId
            } for m in messages
        ]
        return jsonify(messages_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
