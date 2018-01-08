import logging

from flask import Flask
from flask_cors import CORS

from budgetkey_list_manager import make_blueprint

from budgetkey_list_manager.config import auth_server

# Create application
app = Flask(__name__, static_folder=None)

# CORS support
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(make_blueprint(verifyer_args={'auth_endpoint': auth_server}),
                       url_prefix='/')


logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    app.run()
