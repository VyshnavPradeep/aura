from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# SQL Injection vulnerability example
@app.route('/user/<user_id>')
def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    return jsonify(result)

# N+1 query problem example
@app.route('/posts')
def get_posts_with_comments():
    posts = []
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # First query to get all posts
    cursor.execute("SELECT * FROM posts")
    all_posts = cursor.fetchall()
    
    # N+1 problem: separate query for each post
    for post in all_posts:
        cursor.execute(f"SELECT * FROM comments WHERE post_id = {post[0]}")
        comments = cursor.fetchall()
        posts.append({
            'post': post,
            'comments': comments
        })
    
    return jsonify(posts)

# Hardcoded credentials (security issue)
SECRET_KEY = "hardcoded_secret_12345"
API_KEY = "admin_key_98765"

# Inefficient algorithm example
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

@app.route('/fib/<int:n>')
def fibonacci(n):
    result = calculate_fibonacci(n)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
