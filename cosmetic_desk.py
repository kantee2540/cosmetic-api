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
            "error": False,
            "is_saved": True
        }
    else:
        json_format = {
            "status": "item not inserted",
            "error": True,
            "is_saved": False
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
            "is_saved": False,
            "error": False
        }
    else:
        json_format = {
            "status": "error to delete item",
            "is_saved": True,
            "error": True
        }

    return jsonify(json_format)


def get_cosmetic_desk():
    items_set = []
    curr = connect_db().cursor()
    orderby = request.form.get('orderby')
    limit = request.form.get('limit')
    uid = request.headers.get('Authorization')
    user = query_user(uid)
    user_id = user["user_id"]

    sql = """SELECT * FROM cosmetic_desk c, product p, product_brand b, categories ca
    WHERE c.product_id = p.product_id 
    AND p.brand_id = b.brand_id 
    AND p.categories_id = ca.categories_id
    AND c.user_id = '{}'\n""".format(user_id)

    if orderby == "a-z":
        sql += "ORDER BY p.product_name "
    elif orderby == "view":
        sql += "ORDER BY p.View DESC "
    elif orderby == "price":
        sql += "ORDER BY p.product_price DESC "
    else:
        sql += "ORDER BY c.desk_id DESC "

    if limit is not None:
        sql += "LIMIT {}".format(limit)

    curr.execute(sql)

    for i in curr:
        items_set.append(i)

    return jsonify(items_set)


def get_cosmetic_desk_favorite():
    items_set = []
    curr = connect_db().cursor()
    orderby = request.form.get('orderby')
    uid = request.headers.get('Authorization')
    user = query_user(uid)
    user_id = user["user_id"]

    sql = """SELECT * FROM cosmetic_desk c, product p, product_brand b, categories ca
        WHERE c.product_id = p.product_id 
        AND p.brand_id = b.brand_id 
        AND p.categories_id = ca.categories_id
        AND c.user_id = '{}'
        AND c.favorite = 1\n""".format(user_id)

    if orderby == "a-z":
        sql += "ORDER BY p.product_name"
    elif orderby == "view":
        sql += "ORDER BY p.View DESC"
    elif orderby == "price":
        sql += "ORDER BY p.product_price DESC"
    else:
        sql += "ORDER BY c.desk_id DESC"

    curr.execute(sql)

    for i in curr:
        items_set.append(i)

    return jsonify(items_set)


def update_favorite():
    curr = connect_db().cursor()
    desk_id = request.form.get('desk_id')
    favorite = request.form.get('favorite')
    uid = request.headers.get('Authorization')

    sql = """UPDATE cosmetic_desk SET favorite = {} WHERE desk_id = {}""".format(favorite, desk_id)

    status = curr.execute(sql)
    if status and uid is not None:
        json_format = {
            "status": "updated favorite",
            "desk_id": desk_id
        }
    else:
        json_format = {
            "status": "update favorite failed",
            "desk_id": desk_id
        }

    return jsonify(json_format)
