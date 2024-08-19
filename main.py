import firebase_admin
from firebase_admin import auth, credentials, db
from flask import Flask, jsonify, request

from tools import sign_in_with_email_and_password, verify_token

app = Flask(__name__)

cred = credentials.Certificate('jooba-demo-firebase-adminsdk.json')
firebase_admin = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jooba-demo-default-rtdb.europe-west1.firebasedatabase.app/'
})


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        user = auth.create_user(email=email, password=password)
        db.reference(f'users/{user.uid}').set({
            'email': email,
            'uid': user.uid
        })

        return jsonify({'message': 'User created successfully', 'uid': user.uid}), 201

    except auth.EmailAlreadyExistsError:
        return jsonify({'error': 'Sorry, user with this Email already exists'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        token = sign_in_with_email_and_password(email, password)

        return jsonify({"message": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/upload_product', methods=['POST'])
def upload_product():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization header missing or invalid'}), 401

    token = auth_header.split('Bearer ')[1]

    uid = verify_token(token)

    if not uid:
        return jsonify({'error': 'Unauthorized. Invalid token or expired.'}), 401

    data = request.json

    name = data.get('name')
    description = data.get('description')
    category = data.get('category')
    price = data.get('price')

    if not name or not description or not category or not price:
        return jsonify({'error': 'Missing required fields: "name", "description", "category", "price'}), 400

    try:
        product = {
            'name': name,
            'description': description,
            'category': category,
            'price': price,
            'user_id': uid
        }

        product_ref = db.reference('products').push(product)

        return jsonify({'message': 'Product uploaded successfully', 'product_id': product_ref.key}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/user_products', methods=['GET'])
def user_products():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization header missing or invalid'}), 401

    token = auth_header.split('Bearer ')[1]
    uid = verify_token(token)

    if not uid:
        return jsonify({'error': 'Unauthorized. Invalid token or expired.'}), 401

    try:
        products = db.reference('products').order_by_child('user_id').equal_to(uid).get()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization header missing or invalid'}), 401

    token = auth_header.split('Bearer ')[1]
    uid = verify_token(token)

    if not uid:
        return jsonify({'error': 'Unauthorized. Invalid token or expired.'}), 401

    try:
        product_ref = db.reference(f'products/{product_id}')
        product = product_ref.get()

        if product and product.get('user_id') == uid:
            product_ref.delete()
            return jsonify({'message': 'Product deleted successfully'}), 200
        else:
            return jsonify({'error': 'Product not found or you are not authorized to delete it'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/product_info/<product_id>', methods=['GET'])
def product_info(product_id):
    try:
        product = db.reference(f'products/{product_id}').get()

        if product:
            return jsonify(product), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/all_products', methods=['GET'])
def all_products():
    try:
        products = db.reference('products').get()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update_product/<product_id>', methods=['PUT'])
def update_product(product_id):
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization header missing or invalid'}), 401

    token = auth_header.split('Bearer ')[1]
    uid = verify_token(token)

    if not uid:
        return jsonify({'error': 'Unauthorized. Invalid token or expired.'}), 401

    product_ref = db.reference(f'products/{product_id}')
    product = product_ref.get()

    if product and product.get('user_id') == uid:
        data = request.json

        name = data.get('name')
        description = data.get('description')
        category = data.get('category')
        price = data.get('price')

        if not name or not description or not category or not price:
            return jsonify({'error': 'Missing required fields: "name", "description", "category", "price'}), 400

        try:
            product_ref.update(data)
            return jsonify({'message': 'Product updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Product not found or unauthorized'}), 404


@app.route('/search_products', methods=['GET'])
def search_products():
    query = request.args.get('query', '')

    if not query:
        return jsonify({'error': 'Search query not provided'}), 400

    try:
        products = db.reference('products').get()

        if not products:
            return jsonify({'message': 'No products found'}), 404

        result = {k: v for k, v in products.items() if query.casefold() in v.get('name', '').casefold()}

        if result:
            return jsonify(result), 200
        else:
            return jsonify({'message': 'No matching products found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/products_by_category/<category_name>', methods=['GET'])
def products_by_category(category_name):
    try:
        products = db.reference('products').order_by_child('category').equal_to(category_name).get()

        if not products:
            return jsonify({'message': 'No products found in this category'}), 404

        return jsonify(products), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
