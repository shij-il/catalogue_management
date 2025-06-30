from flask import Flask, render_template
from api.catalogue_api import catalogue_api
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app) 

app.register_blueprint(catalogue_api, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 