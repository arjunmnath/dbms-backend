from flask import request, jsonify
from flask_restful import Resource
from api.models import create_connection
from mysql.connector import Error
from api.routes import api

class CategoryResource(Resource):
    def post(self):
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            # Get JSON data from the request
            data = request.get_json()
            category_name = data.get('categoryName')

            if not category_name:
                return {'error': 'categoryName is required'}, 400
            
            # Check if the category already exists
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM categories WHERE categoryName = %s", (category_name,))
            existing_category = cursor.fetchone()
            if existing_category:
                return {'message': 'Category already exists'}, 400
            
            # Insert a new category
            cursor.execute("INSERT INTO categories (categoryName) VALUES (%s)", (category_name,))
            connection.commit()
            return jsonify({'message': 'Category added successfully', 'categoryId': cursor.lastrowid}), 201
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            cursor.close()
            connection.close()

    def get(self):
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM categories")
            categories = cursor.fetchall()
            return jsonify(categories), 200
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            cursor.close()
            connection.close()

class CategoryDetailResource(Resource):
    def get(self, category_id):
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM categories WHERE categoryId = %s", (category_id,))
            category = cursor.fetchone()
            if not category:
                return {'error': 'Category not found'}, 404
            return jsonify(category), 200
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            cursor.close()
            connection.close()

    def put(self, category_id):
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            data = request.get_json()
            category_name = data.get('categoryName')

            if not category_name:
                return {'error': 'categoryName is required'}, 400
            
            cursor = connection.cursor()
            cursor.execute("UPDATE categories SET categoryName = %s WHERE categoryId = %s", (category_name, category_id))
            connection.commit()

            if cursor.rowcount == 0:
                return {'error': 'Category not found'}, 404
            
            return {'message': 'Category updated successfully'}, 200
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            cursor.close()
            connection.close()

    def delete(self, category_id):
        connection = create_connection()
        if not connection:
            return {'error': 'Database connection failed'}, 500
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM categories WHERE categoryId = %s", (category_id,))
            connection.commit()

            if cursor.rowcount == 0:
                return {'error': 'Category not found'}, 404
            
            return {'message': 'Category deleted successfully'}, 200
        except Error as e:
            return {'error': str(e)}, 500
        finally:
            cursor.close()
            connection.close()

# Add the resources to the API
api.add_resource(CategoryResource, '/api/v2/categories')
api.add_resource(CategoryDetailResource, '/api/v2/categories/<int:category_id>')