from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify, current_app as app
import mysql.connector

auth = Blueprint('auth', __name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="SHIJILcim@25",
            database="intern"
        )
        app.logger.info("Database connection established for login.")
        return conn
    except mysql.connector.Error as err:
        app.logger.error(f"Database connection failed during login: {err}")
        raise

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        app.logger.info(f"Login attempt for user: {username}")

        if not username or not password:
            app.logger.warning("Login failed: Username or password missing.")
            return jsonify({'error': 'Username and password required'}), 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and user['password'] == password:
                session['user_id'] = user['id']
                app.logger.info(f"Login successful for user: {username}")
                return jsonify({'message': 'Login successful'}), 200
            else:
                app.logger.warning(f"Invalid login credentials for user: {username}")
                return jsonify({'error': 'Invalid credentials'}), 401

        except Exception as e:
            app.logger.exception("Unexpected error during login.")
            return jsonify({'error': 'Internal server error'}), 500

    return render_template('login.html')

@auth.route('/logout')
def logout():
    user_id = session.get('user_id')
    session.clear()
    app.logger.info(f"User logged out: {user_id}")
    return redirect(url_for('auth.login'))
