from flask import jsonify, request
from connection import connect_db
from user import query_user


def check_product_is_saved():
    curr = connect_db().cursor()
    uid = request.headers.get('Authorization')
    product_id = request.form.get('product_id')
    user = query_user(uid)
    user_id = user['user_id']

    sql = """SELECT *
        FROM cosmetic_desk
        WHERE user_id = {}
        AND product_id = {}""".format(user_id, product_id)

    curr.execute(sql)
    item = curr.fetchone()
    if item is not None:
        json_format = {
            "is_saved": True,
            "product_id": product_id
        }
    else:
        json_format = {
            "is_saved": False
        }
    return jsonify(json_format)


def add_product_to_desk():
    curr = connect_db().cursor()
    uid = request.headers.get('Authorization')
    product_id = request.form.get('product_id')
    user = query_user(uid)
    user_id = user['user_id']

    sql = """INSERT INTO `cosmetic_desk` (`desk_id`, `product_id`, `user_id`) 
    VALUES (NULL, '{}', '{}')""".format(product_id, user_id)

    status = curr.execute(sql)
    if status:
        json_format = {
            "status": "inserted an item",
            "error": False
        }
    else:
        json_format = {
            "status": "item not inserted",
            "error": True
        }

    return jsonify(json_format)


def delete_product_from_desk():
    curr = connect_db().cursor()
    uid = request.headers.get('Authorization')
    product_id = request.form.get('product_id')
    user = query_user(uid)
    user_id = user['user_id']

    sql = """DELETE FROM cosmetic_desk
        WHERE product_id = '{}'
        AND user_id = '{}'""".format(product_id, user_id)

    status = curr.execute(sql)
    if status:
        json_format = {
            "status": "delete item success",
            ""
            "is_saved": False
        }
    else:
        json_format = {
            "status": "error to delete item",
            "is_saved": True
        }

    return jsonify(json_format)


def get_cosmetic_desk():
    curr = connect_db().cursor()
    uid = request.headers.get('Authorization')