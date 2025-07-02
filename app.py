from flask import Flask, render_template, redirect, session, url_for
from flask_cors import CORS
from api.catalogue_api import catalogue_api
from routes.auth import auth

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = '2cb999a6dffcf2d2fe21645888b47e54d7c14738d5bc1bcbf0f49e88a5e6ef8a'
CORS(app)


app.register_blueprint(auth)
app.register_blueprint(catalogue_api, url_prefix='/api')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)