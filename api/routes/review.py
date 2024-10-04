from flask import request, jsonify
from flask_restful import Resource
from mysql.connector import Error
from api.models import create_connection
from api.routes import api

# Review Resource
class ReviewResource(Resource):
    def post(self):
        data = request.get_json()
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO reviews (rating, comment, reviewDate, productId, userId) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (data['rating'], data['comment'], data['reviewDate'], data['productId'], data['userId'])
            )
            connection.commit()
            return {'message': 'Review added successfully'}, 201
        except Error as e:
            return {'error': str(e)}, 400
        finally:
            cursor.close()
            connection.close()

    def put(self, review_id):
        data = request.get_json()
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE reviews 
                SET rating = %s, comment = %s, reviewDate = %s 
                WHERE reviewId = %s
                """,
                (data.get('rating'), data.get('comment'), data.get('reviewDate'), review_id)
            )
            connection.commit()
            if cursor.rowcount == 0:
                return {'error': 'Review not found'}, 404
            
            return {'message': 'Review updated successfully'}, 200
        except Error as e:
            return {'error': str(e)}, 400
        finally:
            cursor.close()
            connection.close()

    def delete(self, review_id):
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM reviews WHERE reviewId = %s",
                (review_id,)
            )
            connection.commit()
            if cursor.rowcount == 0:
                return {'error': 'Review not found'}, 404
            
            return {'message': 'Review deleted successfully'}, 200
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            cursor.close()
            connection.close()

# Product Reviews Resource
class ProductReviewsResource(Resource):
    def get(self, product_id):
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT reviewId, rating, comment, reviewDate, userId FROM reviews WHERE productId = %s",
                (product_id,)
            )
            reviews = cursor.fetchall()
            reviews_list = [
                {
                    'reviewId': r[0],
                    'rating': r[1],
                    'comment': r[2],
                    'reviewDate': r[3].isoformat() if r[3] else None,
                    'userId': r[4]
                } for r in reviews
            ]
            return jsonify(reviews_list)
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            cursor.close()
            connection.close()

# Register Resources with Flask-RESTful
api.add_resource(ReviewResource, '/api/v2/reviews', '/api/reviews/<int:review_id>')
api.add_resource(ProductReviewsResource, '/api/v2/products/<int:product_id>/reviews')
