# Demo Vulnerable Backend Application
# WARNING: This code contains intentional security vulnerabilities for testing purposes
# DO NOT use in production!

from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
import pickle
import subprocess

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded credentials
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"
SECRET_KEY = "my-super-secret-key-12345"

# VULNERABILITY 2: SQL Injection
@app.route('/api/users/<user_id>')
def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # SQL Injection vulnerability - user input directly in query
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return jsonify(user)

# VULNERABILITY 3: SQL Injection with string concatenation
@app.route('/api/search')
def search_users():
    search_term = request.args.get('q', '')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Another SQL injection vulnerability
    query = "SELECT * FROM users WHERE name LIKE '%" + search_term + "%'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)

# VULNERABILITY 4: XSS (Cross-Site Scripting)
@app.route('/api/profile')
def show_profile():
    username = request.args.get('name', 'Guest')
    # XSS vulnerability - user input rendered without escaping
    html = f"<h1>Welcome {username}!</h1>"
    return render_template_string(html)

# VULNERABILITY 5: Command Injection
@app.route('/api/ping')
def ping_server():
    host = request.args.get('host', 'localhost')
    # Command injection vulnerability
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True)
    return jsonify({"output": result.stdout.decode()})

# VULNERABILITY 6: Path Traversal
@app.route('/api/files/<filename>')
def get_file(filename):
    # Path traversal vulnerability - no validation
    file_path = f"./uploads/{filename}"
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# VULNERABILITY 7: Insecure Deserialization
@app.route('/api/load_data', methods=['POST'])
def load_data():
    data = request.get_data()
    # Insecure deserialization - pickle is unsafe
    obj = pickle.loads(data)
    return jsonify({"loaded": str(obj)})

# VULNERABILITY 8: Missing Authentication
@app.route('/api/admin/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # No authentication check - anyone can delete users!
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted"})

# VULNERABILITY 9: Weak Password Hashing
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Weak hashing - using MD5 (deprecated)
    import hashlib
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password_hash}')")
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered"})

# VULNERABILITY 10: Information Disclosure
@app.route('/api/debug')
def debug_info():
    # Exposing sensitive system information
    return jsonify({
        "environment": dict(os.environ),
        "secret_key": SECRET_KEY,
        "database_password": DATABASE_PASSWORD,
        "api_key": API_KEY
    })

# VULNERABILITY 11: No Rate Limiting
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # No rate limiting - vulnerable to brute force attacks
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful", "token": "fake-jwt-token"})
    return jsonify({"message": "Invalid credentials"}), 401

# VULNERABILITY 12: Insecure Direct Object Reference (IDOR)
@app.route('/api/orders/<order_id>')
def get_order(order_id):
    # No authorization check - users can access any order
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM orders WHERE id = {order_id}")
    order = cursor.fetchone()
    conn.close()
    return jsonify(order)

# VULNERABILITY 13: Missing HTTPS/Security Headers
# Flask app running without SSL/TLS
# No security headers configured

if __name__ == '__main__':
    # VULNERABILITY 14: Debug mode in production
    app.run(debug=True, host='0.0.0.0', port=5000)
