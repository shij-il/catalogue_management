from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify
import mysql.connector

auth = Blueprint('auth', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SHIJILcim@25",
        database="intern"
    )

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

       
        if user and user['password'] == password:
            session['user_id'] = user['id']
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
