import mysql.connector

# Connect to MySQL
def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",       # Use your password
        database="inventory_system"
    )

def read_inventory():
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    conn.close()
    return items

def add_product_to_db(pid, name, qty, price):

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (id, name, quantity, price) VALUES (%s, %s, %s, %s)",
                   (pid, name, qty, price))
    conn.commit()
    conn.close()

def delete_product(pid):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id=%s", (pid,))
    conn.commit()
    conn.close()

def update_product(pid, name, qty, price):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET name=%s, quantity=%s, price=%s WHERE id=%s",
                   (name, qty, price, pid))
    conn.commit()
    conn.close()

def low_stock(threshold=5):
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory WHERE quantity < %s", (threshold,))
    items = cursor.fetchall()
    conn.close()
    return items
