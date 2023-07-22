from flask import jsonify
from connection import connect_db


def home_display():
    json_data = {}
    topic_list = []
    topic_sql = """SELECT * FROM today_topic t ORDER BY t.topic_id DESC LIMIT 5"""
    product_list = []
    product_sql = """SELECT * FROM product p LIMIT 5"""
    curr = connect_db().cursor()
    curr.execute(topic_sql)
    for t in curr:
        topic_list.append(t)

    curr.execute(product_sql)
    for p in curr:
        product_list.append(p)

    json_data["topics"] = topic_list
    json_data["latest_product"] = product_list
    json_data["most_popular_product"] = product_list

    return jsonify(json_data)
