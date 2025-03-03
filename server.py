from datetime import datetime, timedelta
from flask import Flask, request, render_template, make_response, redirect
import mysql.connector

app = Flask(__name__)

# Establish the connection to the database
def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="rootpassword",
        database="testdb"
    )

# Create users table (if not exists) and insert a test user if needed
def initialize_db():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL
        )
    """)
    db.commit()
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        db.commit()

    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        content TEXT NOT NULL
        )
    """)
    db.commit()
    cursor.execute("SELECT * FROM posts")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO posts (content) VALUES ('<img src=\"https://upload.wikimedia.org/wikipedia/commons/2/22/Malus_domestica_a1.jpg\">')")
        db.commit()
    db.close()

# Initialize database on startup
initialize_db()

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/posts',methods=['GET'])
def posts():
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM posts")
        result = cursor.fetchall()  # Ensure we fetch all results

        return render_template("posts.html",posts=result)
    finally:
        cursor.close()
        db.close()

@app.route("/posts/delete_post", methods=['GET'])
def delete_post():
    post_id = request.args.get('id','')

    query = f"DELETE FROM posts WHERE id = '{post_id}'"
    
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(query)
        db.commit()
        
        return redirect('/posts')
    finally:
        cursor.close()
        db.close()

@app.route("/posts/new_post", methods=['POST'])
def new_post():
    post_content = request.form.get('content','')

    query = "INSERT INTO posts (content) VALUES (%s)"
    
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(query,(post_content,))
        db.commit()
        
        return redirect('/posts')
    finally:
        cursor.close()
        db.close()

@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Vulnerable SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()  # Ensure we fetch all results
        
        if result:
            expiration = datetime.now() + timedelta(minutes=15)
            resp = make_response("Login successful! <br><br> <button onclick=\"window.location.href = '/'\">Back</button> <br><br> <button onclick=\"window.location.href = '/posts'\">Posts</button>")
            resp.set_cookie('username', result[0][1], expires=expiration)
            resp.set_cookie('password', result[0][2], expires=expiration)
            return resp
        else:
            return "Login failed! <br><br> <button onclick=\"window.location.href = '/'\">Back</button>"
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
