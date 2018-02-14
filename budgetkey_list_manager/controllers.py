from .models import get_list, add_item, create_list, get_items, delete_item, get_list_by_item


def store(permissions, list_name, item):
    user_id = permissions.get("userid")
    if not user_id:
        return False
    if not get_list(list_name, user_id):
        create_list(list_name, user_id)
    add_item(list_name, user_id, item)
    return True


def get(permissions, list_name):
    user_id = permissions.get("userid")
    if not user_id:
        return False
    list = get_list(list_name, user_id)
    if not list:
        return False
    return {"id": list["id"], "items": get_items(list_name, user_id)}


def delete(permissions, item_id):
    user_id = permissions.get("userid")
    if not user_id:
        return False
    list = get_list_by_item(item_id)
    if not list or list["user_id"] != user_id:
        return False
    delete_item(item_id)
    return True
