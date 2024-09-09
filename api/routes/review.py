from flask import request, jsonify
from api.models import db, Review
from sqlalchemy.exc import IntegrityError
from api.routes import appbp

# Write a new review for a product
@appbp.route('/api/reviews', methods=['POST']) #working fine
def create_review():
    data = request.get_json()
    try:
        new_review = Review(
            rating=data['rating'],
            comment=data['comment'],
            reviewDate=data['reviewDate'],
            productId=data['productId'],
            userId=data['userId']
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': 'Review added successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Invalid data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Fetch user reviews for a product
@appbp.route('/api/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    try:
        reviews = Review.query.filter_by(productId=product_id).all()
        reviews_list = [
            {
                'reviewId': r.reviewId,
                'rating': r.rating,
                'comment': r.comment,
                'reviewDate': r.reviewDate.isoformat(),
                'userId': r.userId
            } for r in reviews
        ]
        return jsonify(reviews_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
