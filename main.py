import sqlite3
from datetime import datetime

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

    if not orders:
        print("Список заказов пуст.")
    else:
        for order in orders:
            print(order)

    conn.close()

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

    if order:
        print(order)
    else:
        print('Order not found')

    conn.close()

# Функция для консольного интерфейса
def main():
    while True:
        print("\nВыберите действие:")
        print("1. Просмотреть все заказы")
        print("2. Добавить заказ")
        print("3. Изменить статус заказа")
        print("4. Удалить заказ")
        print("5. Найти заказ по ID")
        print("0. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            view_orders()
        elif choice == '2':
            customer_name = input("Введите имя клиента: ")
            product_list = input("Введите список товаров: ")
            order_status = input("Введите статус заказа: ")
            delivery_info = input("Введите информацию о доставке: ")
            other_attributes = input("Введите другие атрибуты (по желанию): ")
            add_order(customer_name, product_list, order_status, delivery_info, other_attributes)
            print("Заказ добавлен.")
        elif choice == '3':
            order_id = input("Введите ID заказа для изменения статуса: ")
            new_status = input("Введите новый статус заказа: ")
            update_order_status(int(order_id), new_status)
            print("Статус заказа изменен.")
        elif choice == '4':
            order_id = input("Введите ID заказа для удаления: ")
            delete_order(int(order_id))
            print("Заказ удален.")
        elif choice == '5':
            order_id = input("Введите ID заказа для поиска: ")
            find_order_by_id(int(order_id))
        elif choice == '0':
            break
        else:
            print("Некорректный ввод. Попробуйте еще раз.")

if __name__ == "__main__":
    create_table()
    main()