from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Функция для создания таблицы заказов
def create_table():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            order_date TEXT NOT NULL,
            product_list TEXT NOT NULL,
            order_status TEXT NOT NULL,
            delivery_info TEXT,
            other_attributes TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Функция для добавления заказа
def add_order(customer_name, product_list, order_status, delivery_info='', other_attributes=''):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO orders (customer_name, order_date, product_list, order_status, delivery_info, other_attributes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (customer_name, order_date, product_list, order_status, delivery_info, other_attributes))

    conn.commit()
    conn.close()

# Функция для просмотра всех заказов
def view_orders():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()

    conn.close()

    return orders

# Функция для изменения статуса заказа
def update_order_status(order_id, new_status):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE orders SET order_status = ? WHERE order_id = ?', (new_status, order_id))

    conn.commit()
    conn.close()

# Функция для удаления заказа
def delete_order(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM orders WHERE order_id = ?', (order_id,))

    conn.commit()
    conn.close()

# Функция для поиска заказа по ID
def find_order_by_id(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
    order = cursor.fetchone()

    conn.close()

    return order

# API endpoint для создания заказа
@app.route('/orders', methods=['POST'])
def add_order_api():
    """
    Create a new order
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Order
          properties:
            customer_name:
              type: string
              description: Name of the customer
              default: John Doe
            product_list:
              type: string
              description: List of products
              default: Product 1, Product 2
            order_status:
              type: string
              description: Status of the order
              default: Pending
            delivery_info:
              type: string
              description: Delivery information
              default: Express delivery
            other_attributes:
              type: string
              description: Other attributes
              default: Additional details
    responses:
      201:
        description: Order added successfully
      400:
        description: Invalid request
    """
    data = request.json
    customer_name = data.get('customer_name')
    product_list = data.get('product_list')
    order_status = data.get('order_status')
    delivery_info = data.get('delivery_info', '')
    other_attributes = data.get('other_attributes', '')

    add_order(customer_name, product_list, order_status, delivery_info, other_attributes)

    return jsonify({'message': 'Order added successfully'}), 201

# API endpoint для получения всех заказов
@app.route('/orders', methods=['GET'])
def read_orders():
    """
    Get all orders
    ---
    responses:
      200:
        description: List of orders
    """
    orders = view_orders()
    return jsonify(orders)

# API endpoint для изменения статуса заказа
@app.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order(order_id):
    """
    Update order status by ID
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID of the order to update
      - name: body
        in: body
        required: true
        schema:
          id: OrderStatus
          properties:
            new_status:
              type: string
              description: New status of the order
              default: Shipped
    responses:
      200:
        description: Order status updated successfully
      404:
        description: Order not found
    """
    data = request.json
    new_status = data.get('new_status')

    existing_order = find_order_by_id(order_id)
    if existing_order:
        update_order_status(order_id, new_status)
        return {"message": "Order status updated successfully"}
    return jsonify({'error': 'Order not found'}), 404

# API endpoint для удаления заказа
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order_endpoint(order_id):
    """
    Delete an order by ID
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID of the order to delete
    responses:
      200:
        description: Order deleted successfully
      404:
        description: Order not found
    """
    existing_order = find_order_by_id(order_id)
    if existing_order:
        delete_order(order_id)
        return {"message": "Order deleted successfully"}
    return jsonify({'error': 'Order not found'}), 404

# API endpoint для поиска заказа по ID
@app.route('/orders/<int:order_id>', methods=['GET'])
def find_order(order_id):
    """
    Find an order by ID
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID of the order to find
    responses:
      200:
        description: Found order
      404:
        description: Order not found
    """
    order = find_order_by_id(order_id)
    if order:
        return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

if __name__ == '__main__':
    create_table()
    app.run(debug=True)