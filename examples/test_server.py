"""
Vulnerable Test Server - FOR EDUCATIONAL PURPOSES ONLY!
This server intentionally contains vulnerabilities for testing the scanner.
DO NOT use this code in production!
"""

from flask import Flask, request, render_template_string
import sqlite3

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
            max-width: 800px;
            margin: 50px auto;
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
        .warning {
            background: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }
        input, button {
            padding: 10px;
            margin: 5px 0;
            font-size: 16px;
        }
        button {
            background: #5bc0de;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚠️ Vulnerable Test Application</h1>
        
        <div class="warning">
            <strong>WARNING:</strong> This is an intentionally vulnerable application 
            for educational purposes. Never deploy this in production!
        </div>

        <h2>Test SQL Injection</h2>
        <form action="/search" method="GET">
            <input type="text" name="id" placeholder="Enter user ID" />
            <button type="submit">Search User</button>
        </form>

        <h2>Test XSS</h2>
        <form action="/comment" method="GET">
            <input type="text" name="text" placeholder="Enter comment" />
            <button type="submit">Submit Comment</button>
        </form>

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
            role TEXT
        )
    ''')
    
    # Insert sample data
    users = [
        (1, 'admin', 'admin@example.com', 'administrator'),
        (2, 'user1', 'user1@example.com', 'user'),
        (3, 'user2', 'user2@example.com', 'user'),
        (4, 'guest', 'guest@example.com', 'guest'),
    ]
    
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users)
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
    Vulnerable SQL Injection endpoint
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
            result_html = "<table border='1' style='width:100%; border-collapse: collapse;'>"
            result_html += "<tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th></tr>"
            
            for row in results:
                result_html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
            
            result_html += "</table>"
            return render_template_string(HTML_TEMPLATE, result=result_html)
        else:
            return render_template_string(HTML_TEMPLATE, result="No user found")
            
    except Exception as e:
        # INTENTIONALLY VULNERABLE: Exposing SQL errors
        error_msg = f"<span style='color:red'>SQL Error: {str(e)}</span>"
        return render_template_string(HTML_TEMPLATE, result=error_msg)


@app.route('/comment')
def comment():
    """
    Vulnerable XSS endpoint
    Example: /comment?text=<script>alert('XSS')</script>
    """
    user_comment = request.args.get('text', '')
    
    if not user_comment:
        return render_template_string(HTML_TEMPLATE, result="Please enter a comment")
    
    # INTENTIONALLY VULNERABLE: Not escaping user input
    result = f"<p>Your comment: {user_comment}</p>"
    result += "<p><em>Comment submitted successfully!</em></p>"
    
    return render_template_string(HTML_TEMPLATE, result=result)


@app.route('/login')
def login():
    """
    Another vulnerable SQLi endpoint
    Example: /login?username=admin'--&password=anything
    """
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    
    if not username or not password:
        return "Please provide username and password"
    
    try:
        # INTENTIONALLY VULNERABLE
        query = f"SELECT * FROM users WHERE username = '{username}' AND role = '{password}'"
        
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            return f"Login successful! Welcome {result[1]}"
        else:
            return "Login failed"
            
    except Exception as e:
        return f"Database error: {str(e)}"


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚨 VULNERABLE TEST SERVER - EDUCATIONAL USE ONLY")
    print("="*60)
    print("Server starting on http://localhost:5000")
    print("\nTest endpoints:")
    print("  - http://localhost:5000/")
    print("  - http://localhost:5000/search?id=1")
    print("  - http://localhost:5000/comment?text=Hello")
    print("  - http://localhost:5000/login?username=admin&password=test")
    print("\n⚠️  DO NOT use this code in production!")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)