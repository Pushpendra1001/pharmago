from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager, mysql
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    
    if not user_data:
        return None
        
    return User(user_data)

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.password_hash = user_data['password']
        self.first_name = user_data['first_name']
        self.last_name = user_data['last_name']
        self.phone = user_data.get('phone', '')
        self.address = user_data.get('address', '')
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def create_user(username, email, password, first_name, last_name):
        cursor = mysql.connection.cursor()
        password_hash = generate_password_hash(password)
        
        cursor.execute(
            "INSERT INTO users (username, email, password, first_name, last_name) VALUES (%s, %s, %s, %s, %s)",
            (username, email, password_hash, first_name, last_name)
        )
        mysql.connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        
        return user_id
    
    @staticmethod
    def get_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if not user_data:
            return None
            
        return User(user_data)
    
    @staticmethod
    def get_by_username(username):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if not user_data:
            return None
            
        return User(user_data)

class Product:
    @staticmethod
    def get_all_products():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        return products
    
    @staticmethod
    def get_product_by_id(product_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        return product
    
    @staticmethod
    def search_products(query):
        cursor = mysql.connection.cursor()
        search_query = f"%{query}%"
        cursor.execute("SELECT * FROM products WHERE name LIKE %s OR description LIKE %s", 
                      (search_query, search_query))
        products = cursor.fetchall()
        cursor.close()
        return products