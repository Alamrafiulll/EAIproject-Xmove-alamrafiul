import csv
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.csv")
def read_users():
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            users = list(reader)
    return users

def write_user(email, password):
    exists = os.path.exists(USERS_FILE)
    with open(USERS_FILE, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['email', 'password']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({'email': email, 'password': password})

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    users = read_users()
    if any(u['email'] == email for u in users):
        return jsonify({"error": "Email already registered"}), 400
    write_user(email, password)
    return jsonify({"message": "Sign up successful"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    users = read_users()
    user = next((u for u in users if u['email'] == email and u['password'] == password), None)
    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

products = [
    # Men - Nike
    {"id": 1, "name": "Nike Air Max", "gender": "Men", "brand": "Nike", "price": 450, "img": "/static/airmax.jpg"},
    {"id": 2, "name": "Nike React Infinity Run", "gender": "Men", "brand": "Nike", "price": 390, "img": "/static/reactinfinity.jpg"},
    {"id": 3, "name": "Nike ZoomX Vaporfly", "gender": "Men", "brand": "Nike", "price": 599, "img": "/static/zoomxvaporfly.jpg"},
    # Men - Adidas
    {"id": 4, "name": "Adidas UltraBoost", "gender": "Men", "brand": "Adidas", "price": 420, "img": "/static/ultraboost.jpg"},
    {"id": 5, "name": "Adidas NMD_R1", "gender": "Men", "brand": "Adidas", "price": 340, "img": "/static/nmdr1.jpg"},
    {"id": 6, "name": "Adidas ZX 2K Boost", "gender": "Men", "brand": "Adidas", "price": 360, "img": "/static/zx2kboost.jpg"},
    # Men - Puma
    {"id": 7, "name": "Puma Future Rider", "gender": "Men", "brand": "Puma", "price": 260, "img": "/static/futurerider.png"},
    {"id": 8, "name": "Puma RS-X", "gender": "Men", "brand": "Puma", "price": 300, "img": "/static/rsx.png"},
    # Men - New Balance
    {"id": 9, "name": "New Balance 574", "gender": "Men", "brand": "New Balance", "price": 370, "img": "/static/newbalance574.png"},
    {"id": 10, "name": "New Balance Fresh Foam 1080", "gender": "Men", "brand": "New Balance", "price": 470, "img": "/static/freshfoam1080.png"},
    # Women - Nike
    {"id": 11, "name": "Nike Air Force 1", "gender": "Women", "brand": "Nike", "price": 400, "img": "/static/airforce1.png"},
    {"id": 12, "name": "Nike Air Zoom Pegasus", "gender": "Women", "brand": "Nike", "price": 350, "img": "/static/pegasus.png"},
    # Women - Adidas
    {"id": 13, "name": "Adidas Nizza Platform", "gender": "Women", "brand": "Adidas", "price": 250, "img": "/static/nizzaplatform.png"},
    {"id": 14, "name": "Adidas Stan Smith", "gender": "Women", "brand": "Adidas", "price": 320, "img": "/static/stansmith.png"},
    # Women - Puma
    {"id": 15, "name": "Puma Cali", "gender": "Women", "brand": "Puma", "price": 330, "img": "/static/cali.png"},
    {"id": 16, "name": "Puma Mayze", "gender": "Women", "brand": "Puma", "price": 290, "img": "/static/mayze.png"},
    # Women - New Balance
    {"id": 17, "name": "New Balance 327", "gender": "Women", "brand": "New Balance", "price": 340, "img": "/static/nb327.png"},
    {"id": 18, "name": "New Balance FuelCell Propel", "gender": "Women", "brand": "New Balance", "price": 420, "img": "/static/fuelcellpropel.png"}
]

cart = []
orders = []

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route('/api/products', methods=['GET'])
def get_products():
    gender = request.args.get('gender')
    brand = request.args.get('brand')
    filtered = products
    if gender and gender != "All":
        filtered = [p for p in filtered if p['gender'].lower() == gender.lower()]
    if brand and brand != "All":
        filtered = [p for p in filtered if p['brand'].lower() == brand.lower()]
    return jsonify(filtered)


@app.route('/api/brands', methods=['GET'])
def get_brands():
    brands = sorted(list(set([p["brand"] for p in products])))
    return jsonify(["All"] + brands)


@app.route('/api/cart', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_cart():
    global cart
    if request.method == 'GET':
        return jsonify(cart)
    elif request.method == 'POST':
        item = request.json
        for c in cart:
            if c['id'] == item['id']:
                c['qty'] += item.get('qty', 1)
                return jsonify(cart)
        cart.append({**item, 'qty': item.get('qty', 1)})
        return jsonify(cart)
    elif request.method == 'PUT':
        data = request.json
        for c in cart:
            if c['id'] == data['id']:
                c['qty'] = data['qty']
                break
        return jsonify(cart)
    elif request.method == 'DELETE':
        data = request.json
        cart[:] = [c for c in cart if c['id'] != data['id']]
        return jsonify(cart)


@app.route('/api/order', methods=['POST'])
def place_order():
    global orders, cart
    if not cart:
        return jsonify({"error": "Cart is empty"}), 400
    orders.append({"order_id": len(orders)+1, "items": cart.copy()})
    cart.clear()
    return jsonify({"message": "Order placed successfully!"})


@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/api/order', methods=['DELETE'])
def cancel_order():
    global orders
    data = request.get_json()
    order_id = data.get('order_id')
    before = len(orders)
    orders = [o for o in orders if o['order_id'] != order_id]
    if len(orders) < before:
        return jsonify({"message": "Order canceled"})
    else:
        return jsonify({"error": "Order not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
