"""
Vulnerable Test Server - FOR EDUCATIONAL PURPOSES ONLY!
This server intentionally contains vulnerabilities for testing the scanner.
DO NOT use this code in production!
"""

from flask import Flask, request, render_template_string, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# HTML template with intentional vulnerabilities
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Test Application</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 30px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #d9534f; }
        h2 { color: #333; margin-top: 30px; border-bottom: 2px solid #ddd; padding-bottom: 10px; }
        .warning {
            background: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }
        input, textarea, button {
            padding: 10px;
            margin: 5px 0;
            font-size: 14px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        textarea {
            width: 100%;
            font-family: Arial, sans-serif;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
        }
        button {
            background: #5bc0de;
            color: white;
            border: none;
            cursor: pointer;
            width: auto;
            padding: 10px 20px;
        }
        button:hover {
            background: #46b8da;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #17a2b8;
        }
        .endpoint {
            margin: 10px 0;
            padding: 8px;
            background: #f0f0f0;
            border-radius: 4px;
            font-family: monospace;
            font-size: 12px;
            color: #333;
        }
        form {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚠️ Vulnerable Test Application</h1>
        
        <div class="warning">
            <strong>WARNING:</strong> This is an intentionally vulnerable application 
            for educational purposes ONLY. Never deploy this in production!
        </div>

        <h2>1️⃣ SQL Injection - GET Request</h2>
        <form action="/search" method="GET">
            <label>User ID:</label>
            <input type="text" name="id" placeholder="Enter user ID (e.g., 1)" />
            <button type="submit">Search User (GET)</button>
        </form>
        <div class="endpoint">Example: /search?id=1' OR '1'='1</div>

        <h2>2️⃣ SQL Injection - POST Request</h2>
        <form action="/search-post" method="POST">
            <label>User ID:</label>
            <input type="text" name="id" placeholder="Enter user ID" />
            <button type="submit">Search User (POST)</button>
        </form>
        <div class="endpoint">Example: POST /search-post with id=1' OR '1'='1</div>

        <h2>3️⃣ XSS - Reflected (GET)</h2>
        <form action="/comment" method="GET">
            <label>Comment:</label>
            <textarea name="text" placeholder="Enter comment" rows="4"></textarea>
            <button type="submit">Submit Comment (GET)</button>
        </form>
        <div class="endpoint">Example: /comment?text=&lt;script&gt;alert('XSS')&lt;/script&gt;</div>

        <h2>4️⃣ XSS - Reflected (POST)</h2>
        <form action="/comment-post" method="POST">
            <label>Comment:</label>
            <textarea name="text" placeholder="Enter comment" rows="4"></textarea>
            <button type="submit">Submit Comment (POST)</button>
        </form>
        <div class="endpoint">Example: POST /comment-post with text=&lt;img src=x onerror=alert(1)&gt;</div>

        <h2>5️⃣ Authentication Bypass - SQL Injection</h2>
        <form action="/login" method="GET">
            <label>Username:</label>
            <input type="text" name="username" placeholder="Enter username" />
            <label>Password:</label>
            <input type="password" name="password" placeholder="Enter password" />
            <button type="submit">Login</button>
        </form>
        <div class="endpoint">Example: username=admin'-- &amp; password=anything</div>

        {% if result %}
        <div class="result">
            <h3>Result:</h3>
            {{ result|safe }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


# Initialize SQLite database
def init_db():
    """Create a simple vulnerable database"""
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT,
            role TEXT,
            password TEXT
        )
    ''')
    
    # Insert sample data
    users = [
        (1, 'admin', 'admin@example.com', 'administrator', 'admin123'),
        (2, 'user1', 'user1@example.com', 'user', 'pass123'),
        (3, 'user2', 'user2@example.com', 'user', 'pass456'),
        (4, 'guest', 'guest@example.com', 'guest', 'guest'),
    ]
    
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?, ?)', users)
    conn.commit()
    
    return conn


# Global database connection
db = init_db()


@app.route('/')
def index():
    """Home page"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/search')
def search():
    """
    Vulnerable SQL Injection endpoint - GET
    Example: /search?id=1' OR '1'='1
    """
    user_id = request.args.get('id', '')
    
    if not user_id:
        return render_template_string(HTML_TEMPLATE, result="Please enter a user ID")
    
    try:
        # INTENTIONALLY VULNERABLE: Direct string concatenation
        query = f"SELECT * FROM users WHERE id = {user_id}"
        
        cursor = db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            result_html = "<h3>Search Results:</h3>"
            result_html += "<table border='1' style='width:100%; border-collapse: collapse;'>"
            result_html += "<tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th></tr>"
            
            for row in results:
                result_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
            
            result_html += "</table>"
            return render_template_string(HTML_TEMPLATE, result=result_html)
        else:
            return render_template_string(HTML_TEMPLATE, result="<p>No user found</p>")
            
    except Exception as e:
        # INTENTIONALLY VULNERABLE: Exposing SQL errors
        error_msg = f"<span style='color:red'><strong>SQL Error:</strong> {str(e)}</span>"
        return render_template_string(HTML_TEMPLATE, result=error_msg)


@app.route('/comment')
def comment():
    """
    Vulnerable XSS endpoint - GET
    Example: /comment?text=<script>alert('XSS')</script>
    """
    user_comment = request.args.get('text', '')
    
    if not user_comment:
        return render_template_string(HTML_TEMPLATE, result="Please enter a comment")
    
    # INTENTIONALLY VULNERABLE: Not escaping user input
    result = f"<h3>Comment Submitted:</h3><p>Your comment: {user_comment}</p>"
    result += "<p><em>Comment submitted successfully!</em></p>"
    
    return render_template_string(HTML_TEMPLATE, result=result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Vulnerable SQL Injection endpoint - Authentication bypass
    Example: /login?username=admin'--&password=anything
    """
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
    else:
        username = request.args.get('username', '')
        password = request.args.get('password', '')
    
    if not username or not password:
        return render_template_string(HTML_TEMPLATE, result="Please provide username and password")
    
    try:
        # INTENTIONALLY VULNERABLE: Vulnerable to authentication bypass
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        cursor = db.cursor()
        cursor.execute(query)
        result_row = cursor.fetchone()
        
        if result_row:
            result = f"<h3 style='color:green'>✓ Login Successful!</h3>"
            result += f"<p><strong>Welcome {result_row[1]}!</strong></p>"
            result += f"<p>Role: {result_row[3]}</p>"
            result += f"<p>Email: {result_row[2]}</p>"
            return render_template_string(HTML_TEMPLATE, result=result)
        else:
            result = "<h3 style='color:red'>✗ Login Failed</h3>"
            result += "<p>Invalid username or password</p>"
            return render_template_string(HTML_TEMPLATE, result=result)
            
    except Exception as e:
        result = f"<h3 style='color:red'>Error:</h3><p>{str(e)}</p>"
        return render_template_string(HTML_TEMPLATE, result=result)


@app.route('/search-post', methods=['POST'])
def search_post():
    """
    Vulnerable SQL Injection endpoint - POST
    Example: POST /search-post with id=1' OR '1'='1
    """
    user_id = request.form.get('id', '')
    
    if not user_id:
        return render_template_string(HTML_TEMPLATE, result="Please enter a user ID")
    
    try:
        # INTENTIONALLY VULNERABLE: Direct string concatenation with POST parameter
        query = f"SELECT * FROM users WHERE id = {user_id}"
        
        cursor = db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            result_html = "<h3>Search Results:</h3>"
            result_html += "<table border='1' style='width:100%; border-collapse: collapse;'>"
            result_html += "<tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th></tr>"
            
            for row in results:
                result_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
            
            result_html += "</table>"
            return render_template_string(HTML_TEMPLATE, result=result_html)
        else:
            return render_template_string(HTML_TEMPLATE, result="<p>No user found</p>")
            
    except Exception as e:
        error_msg = f"<span style='color:red'><strong>SQL Error:</strong> {str(e)}</span>"
        return render_template_string(HTML_TEMPLATE, result=error_msg)


@app.route('/comment-post', methods=['POST'])
def comment_post():
    """
    Vulnerable XSS endpoint - POST
    Example: POST /comment-post with text=<img src=x onerror=alert(1)>
    """
    user_comment = request.form.get('text', '')
    
    if not user_comment:
        return render_template_string(HTML_TEMPLATE, result="Please enter a comment")
    
    # INTENTIONALLY VULNERABLE: Not escaping POST input
    result = f"<h3>Comment Submitted:</h3><p>Your comment: {user_comment}</p>"
    result += "<p><em>Comment posted successfully!</em></p>"
    
    return render_template_string(HTML_TEMPLATE, result=result)


@app.route('/api/users', methods=['GET'])
def api_users():
    """
    Vulnerable API endpoint - SQLi in GET parameter
    Example: /api/users?filter=1' OR '1'='1
    """
    filter_param = request.args.get('filter', '1')
    
    try:
        # INTENTIONALLY VULNERABLE
        query = f"SELECT id, username, email FROM users WHERE id = {filter_param}"
        
        cursor = db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        return jsonify({
            'status': 'success',
            'data': [{'id': r[0], 'username': r[1], 'email': r[2]} for r in results]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/echo', methods=['GET', 'POST'])
def api_echo():
    """
    Vulnerable API endpoint - XSS in JSON response
    Example: /api/echo?message=<script>alert(1)</script>
    """
    message = request.args.get('message', '') or request.form.get('message', '')
    
    return jsonify({
        'status': 'success',
        'message': message,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'application': 'Vulnerable Test Server',
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚨 VULNERABLE TEST SERVER - EDUCATIONAL USE ONLY")
    print("="*70)
    print("\n📍 Server starting on http://localhost:5000")
    print("\n📋 Test endpoints:")
    print("  - GET:  http://localhost:5000/")
    print("  - GET:  http://localhost:5000/search?id=1")
    print("  - GET:  http://localhost:5000/comment?text=Hello")
    print("  - GET:  http://localhost:5000/login?username=admin&password=test")
    print("  - GET:  http://localhost:5000/api/users?filter=1")
    print("  - GET:  http://localhost:5000/api/echo?message=test")
    print("  - POST: http://localhost:5000/search-post (form: id=1' OR '1'='1)")
    print("  - POST: http://localhost:5000/comment-post (form: text=<script>alert(1)</script>)")
    print("\n⚠️  DO NOT use this code in production!")
    print("⚠️  NEVER expose this server to the internet!")
    print("="*70 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)