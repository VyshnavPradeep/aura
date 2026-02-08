# Database Models
# This file contains database-related code with vulnerabilities

import sqlite3
import os

class Database:
    def __init__(self):
        # VULNERABILITY: Hardcoded database credentials
        self.db_host = "localhost"
        self.db_user = "admin"
        self.db_password = "password123"
        self.connection = None
    
    def connect(self):
        # Using SQLite for demo, but credentials still hardcoded
        self.connection = sqlite3.connect('app.db')
        return self.connection
    
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            # VULNERABILITY: Executing raw queries without parameterization
            cursor.execute(query)
        return cursor.fetchall()
    
    def get_user_by_email(self, email):
        # VULNERABILITY: SQL Injection - string formatting
        query = "SELECT * FROM users WHERE email = '%s'" % email
        return self.execute_query(query)
    
    def update_user_balance(self, user_id, amount):
        # VULNERABILITY: No transaction handling, race condition possible
        current = self.execute_query(f"SELECT balance FROM accounts WHERE user_id = {user_id}")
        new_balance = current[0][0] + amount
        self.execute_query(f"UPDATE accounts SET balance = {new_balance} WHERE user_id = {user_id}")
    
    def search_products(self, search_term):
        # VULNERABILITY: SQL Injection via LIKE clause
        query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%' OR description LIKE '%{search_term}%'"
        return self.execute_query(query)
    
    def delete_old_records(self, table_name, days):
        # VULNERABILITY: SQL Injection via table name
        query = f"DELETE FROM {table_name} WHERE created_at < datetime('now', '-{days} days')"
        return self.execute_query(query)

class UserModel:
    def __init__(self, db):
        self.db = db
    
    def authenticate(self, username, password):
        # VULNERABILITY: Storing passwords in plaintext comparison
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        result = self.db.execute_query(query)
        return result[0] if result else None
    
    def create_user(self, username, email, password):
        # VULNERABILITY: No password hashing
        query = f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')"
        self.db.execute_query(query)
        self.db.connection.commit()
    
    def get_all_users(self):
        # VULNERABILITY: No pagination - can cause memory issues with large datasets
        query = "SELECT * FROM users"
        return self.db.execute_query(query)
    
    def update_user_role(self, user_id, role):
        # VULNERABILITY: No authorization check - anyone can make themselves admin
        query = f"UPDATE users SET role = '{role}' WHERE id = {user_id}"
        self.db.execute_query(query)
        self.db.connection.commit()
