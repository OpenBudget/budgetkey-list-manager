from auth.lib import Verifyer

from flask import Blueprint, request, abort
from flask_jsonpify import jsonpify

from .controllers import store, get, delete
from .models import setup_engine
from .config import db_connection_string

import logging


def make_blueprint(verifyer_args=None, enable_mock_oauth=None):
    """Create blueprint.
    """
    setup_engine(db_connection_string)

    # Create instance
    blueprint = Blueprint('budgetkey_list_manager', 'budgetkey_list_manager')

    verifyer = Verifyer(**verifyer_args)

    # Controller Proxies
    store_controller = store
    get_controller = get
    delete_controller = delete

    def get_permissions():
        token = request.headers.get('auth-token') or request.values.get('jwt')
        try:
            permissions = verifyer.extract_permissions(token)
        except Exception:
            if enable_mock_oauth:
                logging.warning("Failed to verify permissions, continuing with mock permissions")
                permissions = {"authenticated": True, "profile": {"id": str(token)}}
            else:
                raise
        return permissions

    def store_():
        permissions = get_permissions()
        if permissions is False:
            abort(403)
        list_name = request.values.get('list')
        item = request.get_json()
        if None in (list_name, item):
            abort(400)
        return jsonpify(store_controller(permissions, list_name, item))

    def read_():
        permissions = get_permissions()
        if permissions is False:
            abort(403)
        list_name = request.values.get('list')
        if not list_name:
            abort(400)
        return jsonpify(get_controller(permissions, list_name))

    def delete_():
        permissions = get_permissions()
        if permissions is False:
            abort(403)
        list_name = request.values.get('list')
        item_id = request.values.get('item_id')
        if None in (list_name, item_id):
            abort(400)
        return jsonpify(delete_controller(permissions, item_id))


    # Register routes
    blueprint.add_url_rule(
        'list', 'put', store_, methods=['PUT'])
    blueprint.add_url_rule(
        'list', 'delete', delete_, methods=['DELETE'])
    blueprint.add_url_rule(
        'list', 'get', read_, methods=['GET'])

    # Return blueprint
    return blueprint
