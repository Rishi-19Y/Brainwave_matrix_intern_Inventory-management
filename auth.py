import mysql.connector

def register_user(name, phone, age, workplace, branch, username, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # or your MySQL password
        database="inventory_system"
    )
    cursor = conn.cursor()
    query = "INSERT INTO users (name, phone, age, workplace, branch, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (name, phone, age, workplace, branch, username, password)
    try:
        cursor.execute(query, values)
        conn.commit()
        return True, "Registration successful."
    except mysql.connector.Error as e:
        return False, f"Error: {e}"
    finally:
        conn.close()

def authenticate(username, password):
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # <--- UPDATE THIS
    database="inventory_system"
)

    
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True, "Login successful."
    else:
        return False, "Invalid username or password."
