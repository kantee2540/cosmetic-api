from flask import jsonify, request
from connection import connect_db


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
        json_format = {"error": "user not found"}

    return jsonify(json_format)
