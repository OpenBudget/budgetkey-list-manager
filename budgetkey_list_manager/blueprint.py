from auth.lib import Verifyer

from flask import Blueprint, request, abort
from flask_jsonpify import jsonpify

from .controllers import store


def make_blueprint(verifyer_args=None):
    """Create blueprint.
    """

    # Create instance
    blueprint = Blueprint('budgetkey_list_manager', 'budgetkey_list_manager')

    if verifyer_args is None:
        verifyer_args = dict(auth_endpoint='http://auth:8000')
    verifyer = Verifyer(auth_endpoint=verifyer_args.get('auth_endpoint'),
                        public_key=verifyer_args.get('public_key'))

    # Controller Proxies
    store_controller = store

    def store_():
        token = request.headers.get('auth-token') or request.values.get('jwt')
        permissions = verifyer.extract_permissions(token)
        if permissions is False:
            abort(403)
        list_id = request.values.get('list')
        item = request.values.get('item')
        if None in (list_id, item):
            abort(400)
        return jsonpify(store(permissions, list_id, item))

    # Register routes
    blueprint.add_url_rule(
        'list', 'list', store_, methods=['PUT'])
    # blueprint.add_url_rule(
    #     'list', 'list', delete_, methods=['DELETE'])
    # blueprint.add_url_rule(
    #     'list', 'list', read_, methods=['GET'])

    # Return blueprint
    return blueprint
