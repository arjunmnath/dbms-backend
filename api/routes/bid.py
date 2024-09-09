from flask import Blueprint, request, jsonify
from models import db, Bid
from sqlalchemy.exc import IntegrityError
from . import appbp

# Create a new bid
@appbp.route('/api/bids', methods=['POST']) #working fine
def create_bid():
    data = request.get_json()
    try:
        new_bid = Bid(
            bidAmount=data['bidAmount'],
            bidTime=data['bidTime'],
            isWinningBid=data['isWinningBid'],
            userId=data['userId'],
            productId=data['productId']
        )
        db.session.add(new_bid)
        db.session.commit()
        return jsonify({'message': 'Bid placed successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Invalid data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
