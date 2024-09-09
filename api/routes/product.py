from flask import request, jsonify
from flask_restful import Resource
from api.models import db, Category, Product, ProductImage, CatProd
from sqlalchemy.exc import IntegrityError
from . import api

# Resource for managing a single product
class ProductResource(Resource):
    def get(self, product_id):
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

    def put(self, product_id):
        data = request.get_json()
        try:
            product = Product.query.get_or_404(product_id)
            
            product.title = data.get('title', product.title)
            product.description = data.get('description', product.description)
            product.condition = data.get('condition', product.condition)
            product.initialBid = data.get('initialBid', product.initialBid)
            product.status = data.get('status', product.status)
            product.startTime = data.get('startTime', product.startTime)
            product.endTime = data.get('endTime', product.endTime)

            # Update product images if provided
            if 'images' in data:
                ProductImage.query.filter_by(productId=product.productId).delete()
                for image_url in data['images']:
                    new_product_img = ProductImage(productId=product.productId, imageURL=image_url)
                    db.session.add(new_product_img)

            db.session.commit()
            return jsonify({'message': 'Product updated successfully'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Error updating product'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, product_id):
        try:
            product = Product.query.get_or_404(product_id)
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# Resource for managing product collections
class ProductListResource(Resource):
    def get(self):
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

    def post(self):
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
            category = Category.query.get_or_404(categoryId)

            db.session.add(new_product)
            db.session.commit()

            CatProd_entry = CatProd(categoryId=categoryId, productId=new_product.productId)
            db.session.add(CatProd_entry)
            db.session.commit()

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


# Resource for managing products by category
class CategoryProductsResource(Resource):
    def get(self, category_id):
        try:
            products = db.session.query(Product).join(CatProd).filter(CatProd.c.categoryId == category_id).all()
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


# Register resources with the API
api.add_resource(ProductResource, '/api/v2/products/<int:product_id>')
api.add_resource(ProductListResource, '/api/v2/products')
api.add_resource(CategoryProductsResource, '/api/v2/categories/<int:category_id>/products')
