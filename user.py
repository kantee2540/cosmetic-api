from flask import jsonify, request, make_response, abort
from connection import connect_db
import os


def query_user(uid):
    curr = connect_db().cursor()
    sql = "SELECT * FROM user WHERE uid = '{}'".format(uid)

    curr.execute(sql)
    user = curr.fetchone()
    return user


def get_user_profile():
    uid = request.form.get('uid')
    user = query_user(uid)

    if user is not None:
        json_format = user
    else:
        error_response = make_response(jsonify(error="User not found"), 400)
        abort(error_response)

    return jsonify(json_format)


def create_user():
    first_name = f"'{request.form.get('first_name')}'" if request.form.get('first_name') is not None else "NULL"
    last_name = f"'{request.form.get('last_name')}'" if request.form.get('last_name') is not None else "NULL"
    nickname = request.form.get('nickname')
    email = request.form.get('email')
    uid = request.form.get('uid')

    curr = connect_db().cursor()

    # Check E-mail is unique
    check_email_sql = f"SELECT COUNT(*) FROM user WHERE email = '{email}'"
    count_email = curr.execute(check_email_sql)
    if count_email > 0:
        error_response = make_response(jsonify(error="This email is already registered."), 400)
        abort(error_response)

    sql = """INSERT INTO `user` (`user_id`, `first_name`, `last_name`, `nickname`, `email`, `uid`, `profilepic`) 
        VALUES (NULL, {}, {}, '{}', '{}', '{}', '')""".format(first_name, last_name, nickname, email, uid)
    status = curr.execute(sql)

    if status:
        json_format = {
            "status": "created user",
            "email": email,
            "error": False
        }

    else:
        json_format = {
            "status": "error create user",
            "email": email,
            "error": True
        }

    return jsonify(json_format)


def update_user():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    nickname = request.form.get('nickname')
    email = request.form.get('email')
    uid = request.form.get('uid')

    curr = connect_db().cursor()
    sql = """UPDATE `user` 
    SET first_name = '{}', last_name = '{}', nickname = '{}' 
    WHERE uid = '{}';""" \
        .format(first_name, last_name, nickname, uid)
    status = curr.execute(sql)

    if status:
        json_format = {
            "status": "updated user",
            "email": email,
            "error": False
        }

    else:
        json_format = {
            "status": "error update user",
            "email": email,
            "error": True
        }

    return jsonify(json_format)


def delete_user():
    uid = request.headers.get('Authorization')
    user = query_user(uid)
    user_id = user["user_id"]

    curr = connect_db().cursor()
    sql = """DELETE FROM user WHERE user_id = {}""".format(user_id)
    status = curr.execute(sql)

    if status:
        json_format = {
            "status": "deleted user",
            "error": False
        }
    else:
        json_format = {
            "status": "error delete user",
            "error": True
        }

    return jsonify(json_format)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_is_uploaded(user_id):
    curr = connect_db().cursor()
    sql = """SELECT * FROM user WHERE user_id = {}""".format(user_id)
    curr.execute(sql)
    data = curr.fetchone()
    if data["profilepic"] != "":
        return True
    else:
        return False


def upload_profile():
    file = request.files["image"]
    uid = request.headers.get('Authorization')
    user = query_user(uid)
    user_id = user["user_id"]

    if file and allowed_file(file.filename):
        extension = file.filename.rsplit('.', 1)[1].lower()
        filename = str(user_id) + "." + extension
        file.save(os.path.join("./static/profile", filename))
        profile_url = request.url_root + "profile_img/" + filename

        if not check_is_uploaded(user_id):
            curr = connect_db().cursor()
            sql = """UPDATE user SET profilepic = '{}' WHERE user_id = {}""".format(profile_url, user_id)
            status = curr.execute(sql)
            if status:
                json_format = {
                    "status": "upload image success",
                    "profile_url": profile_url,
                    "error": False
                }
            else:
                json_format = {
                    "status": "update database failed",
                    "error": True,
                    "sql": sql
                }
        else:
            curr = connect_db().cursor()
            sql = """UPDATE user SET profilepic = '{}' WHERE user_id = {}""".format(profile_url, user_id)
            curr.execute(sql)
            json_format = {
                "status": "changed image success",
                "profile_url": profile_url,
                "error": False
            }

    else:
        json_format = {
            "status": "update failed",
            "error": True
        }

    return jsonify(json_format)
