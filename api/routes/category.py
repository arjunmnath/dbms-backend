from flask import request, jsonify
from models import db, Category
from sqlalchemy.exc import IntegrityError
from . import appbp

#Creates new category
@appbp.route('/api/categories', methods=['POST']) #working fine
def add_category():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Extract category name
        category_name = data['categoryName']
        
        # Check if the category already exists
        existing_category = Category.query.filter_by(categoryName=category_name).first()
        if existing_category:
            return jsonify({'message': 'Category already exists'}), 400
        
        # Create a new category instance
        new_category = Category(categoryName=category_name)
        
        # Add the new category to the database
        db.session.add(new_category)
        db.session.commit()
        
        # Return success response
        return jsonify({'message': 'Category added successfully', 'categoryId': new_category.categoryId}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Fetch categories
@appbp.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        # Fetch all categories from the database
        categories = Category.query.all()
        
        # Prepare response data
        categories_list = [
            {
                'categoryId': c.categoryId,
                'categoryName': c.categoryName
            } for c in categories
        ]
        
        return jsonify(categories_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
