from flask import request, jsonify
from flask_restful import Resource
from api.models import create_connection
from api.routes import api
from mysql.connector import Error

class BidResource(Resource):
    def post(self):
        try:
            # Parse the incoming JSON data
            data = request.get_json()

            # Validate input data
            required_fields = ['bidAmount', 'bidTime', 'isWinningBid', 'userId', 'productId']
            for field in required_fields:
                if field not in data:
                    return {'error': f'Missing required field: {field}'}, 400
            
            # Check data types
            if not isinstance(data['bidAmount'], (int, float)):
                return {'error': 'bidAmount must be a number'}, 400
            if not isinstance(data['isWinningBid'], bool):
                return {'error': 'isWinningBid must be a boolean'}, 400
            
            # Establish database connection
            connection = create_connection()
            cursor = connection.cursor()

            # Prepare the insert query
            insert_query = """
            INSERT INTO bids (bidAmount, bidTime, isWinningBid, userId, productId)
            VALUES (%s, %s, %s, %s, %s)
            """
            bid_values = (
                data['bidAmount'],
                data['bidTime'],  # Ensure that this is in the correct format (e.g., 'YYYY-MM-DD HH:MM:SS')
                data['isWinningBid'],
                data['userId'],
                data['productId']
            )
            
            # Execute the query
            cursor.execute(insert_query, bid_values)
            connection.commit()

            # Get the ID of the newly created bid
            bid_id = cursor.lastrowid
            
            return {
                'message': 'Bid placed successfully',
                'bidId': bid_id,
                'bidAmount': data['bidAmount'],
                'bidTime': data['bidTime'],
                'isWinningBid': data['isWinningBid'],
                'userId': data['userId'],
                'productId': data['productId']
            }, 201

        except Error as err:
            # Handle MySQL-specific errors
            return {'error': f'MySQL error: {str(err)}'}, 500
        except Exception as e:
            # Handle general exceptions
            return {'error': str(e)}, 500
        finally:
            # Ensure the cursor and connection are closed
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class BidDetailResource(Resource):
    def get(self, bid_id):
        try:
            # Establish database connection
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)  # Use dictionary for easier access to columns
            
            # Prepare the select query
            select_query = "SELECT * FROM bids WHERE bidId = %s"
            cursor.execute(select_query, (bid_id,))
            bid = cursor.fetchone()  # Fetch one result
            
            if not bid:
                return {'error': 'Bid not found'}, 404
            
            return {
                'bidId': bid['bidId'],
                'bidAmount': float(bid['bidAmount']),
                'bidTime': bid['bidTime'].isoformat() if bid['bidTime'] else None,  # Handle None case
                'isWinningBid': bid['isWinningBid'],
                'userId': bid['userId'],
                'productId': bid['productId']
            }
        except Error as err:
            # Handle MySQL-specific errors
            return {'error': f'MySQL error: {str(err)}'}, 500
        except Exception as e:
            # Handle general exceptions
            return {'error': str(e)}, 500
        finally:
            # Ensure the cursor and connection are closed
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete(self, bid_id):
        try:
            # Establish database connection
            connection = create_connection()
            cursor = connection.cursor()

            # Prepare the delete query
            delete_query = "DELETE FROM bids WHERE bidId = %s"
            cursor.execute(delete_query, (bid_id,))
            connection.commit()
            
            if cursor.rowcount == 0:
                return {'error': 'Bid not found'}, 404
            
            return {'message': 'Bid deleted successfully'}
        except Error as err:
            # Handle MySQL-specific errors
            return {'error': f'MySQL error: {str(err)}'}, 500
        except Exception as e:
            # Handle general exceptions
            return {'error': str(e)}, 500
        finally:
            # Ensure the cursor and connection are closed
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class ProductBidsResource(Resource):
    def get(self, product_id):
        try:
            # Establish database connection
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)  # Use dictionary for easier access to columns
            
            # Prepare the select query
            select_query = "SELECT * FROM bids WHERE productId = %s"
            cursor.execute(select_query, (product_id,))
            bids = cursor.fetchall()  # Fetch all results
            
            # Prepare the response
            bids_list = [
                {
                    'bidId': bid['bidId'],
                    'bidAmount': float(bid['bidAmount']),
                    'bidTime': bid['bidTime'].isoformat() if bid['bidTime'] else None,  # Handle None case
                    'isWinningBid': bid['isWinningBid'],
                    'userId': bid['userId']
                } for bid in bids
            ]
            
            return bids_list if bids_list else [], 200  # Return an empty list if no bids found
        except Error as err:
            # Handle MySQL-specific errors
            return {'error': f'MySQL error: {str(err)}'}, 500
        except Exception as e:
            # Handle general exceptions
            return {'error': str(e)}, 500
        finally:
            # Ensure the cursor and connection are closed
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class UserBidsResource(Resource):
    def get(self, user_id):
        try:
            # Establish database connection
            connection = create_connection()
            cursor = connection.cursor(dictionary=True)  # Use dictionary for easier access to columns
            
            # Prepare the select query
            select_query = "SELECT * FROM bids WHERE userId = %s"
            cursor.execute(select_query, (user_id,))
            bids = cursor.fetchall()  # Fetch all results
            
            # Prepare the response
            bids_list = [
                {
                    'bidId': bid['bidId'],
                    'bidAmount': float(bid['bidAmount']),
                    'bidTime': bid['bidTime'].isoformat() if bid['bidTime'] else None,  # Handle None case
                    'isWinningBid': bid['isWinningBid'],
                    'productId': bid['productId']
                } for bid in bids
            ]
            
            return bids_list if bids_list else [], 200  # Return an empty list if no bids found
        except Error as err:
            # Handle MySQL-specific errors
            return {'error': f'MySQL error: {str(err)}'}, 500
        except Exception as e:
            # Handle general exceptions
            return {'error': str(e)}, 500
        finally:
            # Ensure the cursor and connection are closed
            if cursor:
                cursor.close()
            if connection:
                connection.close()

# Add the resources to the API
api.add_resource(BidResource, '/api/v2/bids')
api.add_resource(BidDetailResource, '/api/v2/bids/<int:bid_id>')
api.add_resource(ProductBidsResource, '/api/v2/products/<int:product_id>/bids')
api.add_resource(UserBidsResource, '/api/v2/users/<int:user_id>/bids')
