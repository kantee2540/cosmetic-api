from flask import jsonify, request
from connection import connect_db
from user import query_user


def beauty_set():
    beauty_sets = []

    limit = request.values.get('limit')
    top_limit = request.values.get('top_limit')
    topic_code = request.values.get('topic_code')

    curr = connect_db().cursor()
    sql = """SELECT * 
            FROM today_topic t
            JOIN user u ON t.user_id = u.user_id\n"""

    if limit is not None:
        sql += "ORDER BY RAND() limit {}".format(limit)
    elif top_limit is not None:
        sql += "ORDER BY t.view_count DESC limit {}".format(top_limit)
    elif topic_code is not None:
        sql += "WHERE topic_code = '{}'".format(topic_code)

    curr.execute(sql)
    for i in curr:
        beauty_sets.append(i)

    return jsonify(beauty_sets)


def show_beauty_set(topic_id):
    package = []
    curr = connect_db().cursor()
    curr_like = connect_db().cursor()
    curr_package = connect_db().cursor()
    uid = request.headers.get('Authorization')

    sql = """SELECT * FROM today_topic t
            JOIN user u ON t.user_id = u.user_id
            WHERE t.topic_id = {}""".format(topic_id)

    sql_like = """SELECT count(*) as like_count
                 FROM topic_like 
                 WHERE topic_id = {}""".format(topic_id)

    sql_package = """SELECT p.product_id, p.product_name, p.product_price, p.product_img, c.categories_name
                    FROM packages k, product p, today_topic t, categories c
                    WHERE k.product_id = p.product_id
                    AND k.topic_id = t.topic_id 
                    AND p.categories_id = c.categories_id
                    AND t.topic_id = {}""".format(topic_id)

    if uid != "":
        is_saved = check_saved(uid, topic_id)
    else:
        is_saved = False

    curr.execute(sql)
    curr_like.execute(sql_like)
    curr_package.execute(sql_package)

    for i in curr_package:
        package.append(i)

    like_count = curr_like.fetchone()["like_count"]

    json_format = {
        "data": curr.fetchone(),
        "packages": package,
        "like_count": like_count,
        "is_saved": is_saved
    }

    return jsonify(json_format)


def check_saved(uid, topic_id):
    user = query_user(uid)
    user_id = user["user_id"]
    curr_saved = connect_db().cursor()
    sql = """SELECT * FROM save_today_topic 
            WHERE topic_id = '{}' AND user_id = '{}'""".format(topic_id, user_id)
    curr_saved.execute(sql)
    item = curr_saved.fetchall()
    if len(item) > 0:
        return True
    else:
        return False


def save_beauty_set():
    curr = connect_db().cursor()
    uid = request.headers.get('Authorization')
    topic_id = request.form.get('topic_id')
    user = query_user(uid)
    user_id = user["user_id"]

    sql = """INSERT INTO save_today_topic(topic_id, user_id)
     VALUES({}, {})""".format(topic_id, user_id)
    status = curr.execute(sql)
    if status:
        json_format = {
            "status": "inserted to save beauty set",
            "error": False
        }
    else:
        json_format = {
            "status": "failed to save beauty set",
            "error": True
        }

    return jsonify(json_format)


def delete_beauty_set():
    curr = connect_db().cursor()
    uid = request.headers.get('Authorization')
    topic_id = request.form.get('topic_id')
    user = query_user(uid)
    user_id = user["user_id"]

    sql = """DELETE FROM save_today_topic
         WHERE topic_id = {}
         AND user_id = {}""".format(topic_id, user_id)
    status = curr.execute(sql)
    if status:
        json_format = {
            "status": "deleted from save beauty set",
            "error": False
        }
    else:
        json_format = {
            "status": "failed to delete beauty set",
            "error": True
        }

    return jsonify(json_format)


def beauty_check_liked():
    uid = request.headers.get('Authorization')
    topic_id = request.form.get('topic_id')
    is_liked = beauty_set_is_liked(uid, topic_id)
    current_like = get_like_count(topic_id)

    json_format = {
        "is_liked": is_liked,
        "current_like": current_like,
    }

    return jsonify(json_format)


def set_like():
    curr = connect_db().cursor()
    uid = request.headers.get('Authorization')
    topic_id = request.form.get('topic_id')
    user = query_user(uid)
    user_id = user["user_id"]

    sql = """INSERT INTO topic_like(topic_id, user_id) VALUES('{}', '{}')""".format(topic_id, user_id)

    status = curr.execute(sql)
    if status:
        current_like = get_like_count(topic_id)
        json_format = {
            "status": "liked",
            "is_liked": True,
            "current_like": current_like,
            "error": False
        }

    else:
        json_format = {
            "status": "error to liked",
            "is_liked": False,
            "error": True
        }

    return jsonify(json_format)


def set_unlike():
    curr = connect_db().cursor()
    uid = request.headers.get('Authorization')
    topic_id = request.form.get('topic_id')
    user = query_user(uid)
    user_id = user["user_id"]

    sql = """DELETE FROM topic_like WHERE topic_id = {} AND user_id = {}""".format(topic_id, user_id)

    status = curr.execute(sql)
    if status:
        current_like = get_like_count(topic_id)
        json_format = {
            "status": "unliked",
            "is_liked": False,
            "current_like": current_like,
            "error": False
        }

    else:
        json_format = {
            "status": "error to liked",
            "is_liked": False,
            "error": True
        }

    return jsonify(json_format)


def beauty_set_is_liked(uid, topic_id):
    curr = connect_db().cursor()

    user = query_user(uid)
    user_id = user["user_id"]

    sql = """SELECT * FROM topic_like 
    WHERE user_id = {} 
    AND topic_id = {}""".format(user_id, topic_id)

    curr.execute(sql)

    if len(curr.fetchall()) > 0:
        return True
    else:
        return False


def get_like_count(topic_id):
    curr_like = connect_db().cursor()
    sql_like = """SELECT count(*) as like_count
                     FROM topic_like 
                     WHERE topic_id = {}""".format(topic_id)
    curr_like.execute(sql_like)
    like_count = curr_like.fetchone()["like_count"]
    return like_count


def get_beauty_set():
    saved_beauty_set = []
    curr = connect_db().cursor()
    order = request.form.get('orderby')
    uid = request.headers.get('Authorization')
    user = query_user(uid)
    user_id = user["user_id"]

    sql = """SELECT * FROM save_today_topic s, today_topic t 
    WHERE s.topic_id = t.topic_id 
    AND s.user_id = {} \n""".format(user_id)

    if order == "a-z":
        sql += "ORDER BY t.topic_name"
    elif order == "view":
        sql += "ORDER BY t.view_count DESC"
    else:
        sql += "ORDER BY s.save_id DESC"

    curr.execute(sql)
    for i in curr:
        saved_beauty_set.append(i)

    return jsonify(saved_beauty_set)


def get_my_beauty_set():
    my_beauty_sets = []
    curr = connect_db().cursor()
    uid = request.headers.get('Authorization')
    user = query_user(uid)
    user_id = user["user_id"]

    sql = """SELECT * 
            FROM today_topic t
            JOIN user u ON t.user_id = u.user_id
            WHERE u.user_id = {}""".format(user_id)

    curr.execute(sql)
    for i in curr:
        my_beauty_sets.append(i)

    return jsonify(my_beauty_sets)
