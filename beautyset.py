from flask import jsonify, request
from connection import connect_db


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
        "is_saved": False
    }

    return jsonify(json_format)
