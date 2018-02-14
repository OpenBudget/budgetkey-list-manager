import os

# Auth server (to get the public key)
auth_server = os.environ.get('AUTH_SERVER')

enable_mock_oauth = (os.environ.get("ENABLE_MOCK_OAUTH") == "1")

db_connection_string = os.environ.get('DATABASE_URL')
