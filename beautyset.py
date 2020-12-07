from flask import jsonify, request
from connection import connect_db
from user import query_user
from random import shuffle
import os


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


def delete_beauty_save_set():
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
            WHERE u.user_id = {}
            ORDER BY topic_id DESC""".format(user_id)

    curr.execute(sql)
    for i in curr:
        my_beauty_sets.append(i)

    return jsonify(my_beauty_sets)


def convert_to_list(product_set):
    str1 = product_set.replace(']', '').replace('[', '')
    product_list = str1.split(",")
    return product_list


def random_letter(num):
    string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    string_list = list(string)
    shuffle(string_list)
    string = ''.join(string_list)
    return string[0:num]


def add_beauty_set():
    topic_name = request.values.get('topic_name')
    topic_description = request.values.get('topic_desc')
    product_set = request.values.get('productset')
    topic_image = request.files["topic_image"]
    topic_code = random_letter(6)
    uid = request.headers.get('Authorization')
    user = query_user(uid)
    user_id = user["user_id"]
    json_format = {}

    curr = connect_db().cursor()
    sql = """INSERT INTO today_topic(topic_name, topic_description, topic_code, user_id, view_count)
    VALUES ('{}', '{}', '{}', '{}', 0)""".format(topic_name, topic_description, topic_code, user_id)
    status = curr.execute(sql)

    if topic_image and status:

        curr_topic = connect_db().cursor()
        sql = """SELECT topic_id FROM today_topic WHERE topic_name = '{}' """.format(topic_name)
        curr_topic.execute(sql)
        topic = curr_topic.fetchone()
        topic_id = topic["topic_id"]

        extension = topic_image.filename.rsplit('.', 1)[1].lower()
        filename = str(topic_id) + "." + extension
        topic_image.save(os.path.join("static/beauty_set_cover", filename))
        profile_url = request.url_root + "beautyset_cover/" + filename
        curr_update = connect_db().cursor()
        sql = """UPDATE today_topic SET topic_img = '{}' WHERE topic_id = {} """.format(profile_url, topic_id)
        update_status = curr_update.execute(sql)
        if update_status:
            error = False
            if product_set != "[]":
                product_set_list = convert_to_list(product_set)
                curr_add_product = connect_db().cursor()
                for j in product_set_list:
                    sql = """INSERT INTO packages(product_id, topic_id) VALUES ({}, {})""".format(j, topic_id)
                    added = curr_add_product.execute(sql)
                    if added:
                        continue
                    else:
                        error = True
                        break

            if not error:
                json_format["status"] = "add beauty set success"
                json_format["topic_code"] = topic_code
                json_format["error"] = False
            else:
                json_format["status"] = "add beauty set packages failed"
                json_format["error"] = True
        else:
            json_format["status"] = "add beauty set failed"
            json_format["error"] = True
    else:
        json_format["status"] = "add beauty set failed"
        json_format["error"] = True

    return jsonify(json_format)


def delete_beauty_set():
    topic_id = request.values.get('topic_id')
    uid = request.headers.get('Authorization')
    user = query_user(uid)

    if user is not None:
        curr = connect_db().cursor()
        sql = """DELETE FROM today_topic 
                WHERE topic_id = {}""".format(topic_id)

        status = curr.execute(sql)

        if status:
            file = "{}.jpg".format(topic_id)
            os.remove("static/beauty_set_cover/{}".format(file))
            json_format = {
                "status": "Remove beauty set success",
                "error": False
            }

        else:
            json_format = {
                "status": "Remove beauty set failed",
                "error": True
            }
    else:
        json_format = {
            "status": "Authorization failed",
            "error": True
        }

    return jsonify(json_format)
