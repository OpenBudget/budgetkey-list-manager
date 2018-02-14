import logging

from flask import Flask
from flask_cors import CORS

from budgetkey_list_manager import make_blueprint

from budgetkey_list_manager.config import auth_server, enable_mock_oauth

# Create application
app = Flask(__name__, static_folder=None)

# CORS support
CORS(app, supports_credentials=True)

# Register blueprints
verifyer_args = {'auth_endpoint': auth_server}
if enable_mock_oauth:
    verifyer_args["public_key"] = "mock-public-key"
app.register_blueprint(make_blueprint(verifyer_args=verifyer_args,
                                      enable_mock_oauth=enable_mock_oauth),
                       url_prefix='/')


logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    app.run(port=5050)
