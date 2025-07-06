import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask, render_template, redirect, session, url_for
from flask_cors import CORS
from flasgger import Swagger

from api.catalogue_api import catalogue_api
from routes.auth import auth

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = '2cb999a6dffcf2d2fe21645888b47e54d7c14738d5bc1bcbf0f49e88a5e6ef8a'
CORS(app)


if not os.path.exists('logs'):
    os.makedirs('logs')

log_handler = RotatingFileHandler('logs/catalogue_app.log', maxBytes=100000, backupCount=3)
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)


swagger_template_path = Path("swagger.yml")
swagger = Swagger(app, template_file=str(swagger_template_path))


app.register_blueprint(auth)
app.register_blueprint(catalogue_api, url_prefix='/api')


@app.route('/')
def index():
    if 'user_id' not in session:
        app.logger.info("Anonymous user tried to access dashboard. Redirecting to login.")
        return redirect(url_for('auth.login'))
    app.logger.info(f"User session active. Serving dashboard.")
    return render_template('index.html')


if __name__ == '__main__':
    app.logger.info("Swagger UI available at: http://127.0.0.1:5000/apidocs/")
    app.run(debug=True)
