from flask import request, jsonify
from api.models import db, Category, Product, ProductImage, CatProd
from sqlalchemy.exc import IntegrityError
from . import appbp

# Post a new product
@appbp.route('/api/products', methods=['POST']) #working fine
def create_product():
    data = request.get_json()
    try:
        new_product = Product(
            title=data['title'],
            description=data['description'],
            condition=data['condition'],
            initialBid=data['initialBid'],
            status=data['status'],
            startTime=data['startTime'],
            endTime=data['endTime'],
            userId=data['userId']
        )
        
        categoryId = data['categoryId']

        # Fetch the category by ID to ensure it exists
        category = Category.query.get_or_404(categoryId)

        db.session.add(new_product)
        db.session.commit()

        # Associate the product with the category
        CatProd_entry = CatProd(categoryId=categoryId, productId=new_product.productId)
        db.session.add(CatProd_entry)
        db.session.commit()

        # Optionally handle product images if provided
        if 'images' in data:
            for image_url in data['images']:
                new_product_img = ProductImage(productId=new_product.productId, imageURL=image_url)
                db.session.add(new_product_img)
            db.session.commit()

        return jsonify({'message': 'Product created successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Error creating product'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Fetch products by category
@appbp.route('/api/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    try:
        # Fetch the category with the given ID
        category = Category.query.get_or_404(category_id)
        
        # Fetch products associated with the category
        products = db.session.query(Product).join(CatProd).filter(CatProd.c.categoryId == category_id).all()
        
        # Prepare response data
        products_list = [
            {
                'productId': p.productId,
                'title': p.title,
                'description': p.description,
                'condition': p.condition,
                'initialBid': float(p.initialBid),
                'currentBidPrice': float(p.currentBidPrice),
                'status': p.status,
                'startTime': p.startTime.isoformat(),
                'endTime': p.endTime.isoformat(),
                'images': [{'imageURL': img.imageURL} for img in p.product_imgs]
            } for p in products
        ]
        
        return jsonify(products_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Fetch products by category name
@appbp.route('/api/categories/name/<string:category_name>/products', methods=['GET'])
def get_products_by_category_name(category_name):
    try:
        # Fetch the category with the given name
        category = Category.query.filter_by(categoryName=category_name).first_or_404()
        
        # Fetch products associated with the category
        products = db.session.query(Product).join(CatProd).filter(CatProd.c.categoryId == category.categoryId).all()
        
        # Prepare response data
        products_list = [
            {
                'productId': p.productId,
                'title': p.title,
                'description': p.description,
                'condition': p.condition,
                'initialBid': float(p.initialBid),
                'currentBidPrice': float(p.currentBidPrice),
                'status': p.status,
                'startTime': p.startTime.isoformat(),
                'endTime': p.endTime.isoformat(),
                'images': [{'imageURL': img.imageURL} for img in p.product_imgs]
            } for p in products
        ]
        
        return jsonify(products_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Fetch all active products
@appbp.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.filter_by(status='active').all()
        products_list = [
            {
                'productId': p.productId,
                'title': p.title,
                'description': p.description,
                'initialBid': float(p.initialBid),
                'currentBidPrice': float(p.currentBidPrice),
                'startTime': p.startTime.isoformat(),
                'endTime': p.endTime.isoformat(),
                'images': [{'imageURL': img.imageURL} for img in p.product_imgs]
            } for p in products
        ]
        return jsonify(products_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Fetch a single product by ID
@appbp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        product_data = {
            'productId': product.productId,
            'title': product.title,
            'description': product.description,
            'condition': product.condition,
            'initialBid': float(product.initialBid),
            'currentBidPrice': float(product.currentBidPrice),
            'status': product.status,
            'startTime': product.startTime.isoformat(),
            'endTime': product.endTime.isoformat(),
            'images': [{'imageURL': img.imageURL} for img in product.product_imgs]
        }
        return jsonify(product_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
