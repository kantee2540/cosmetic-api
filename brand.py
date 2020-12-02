from flask import jsonify
from connection import connect_db


def brand():
    brands_set = []
    curr = connect_db().cursor()

    sql = "SELECT * FROM product_brand"

    curr.execute(sql)
    for i in curr:
        brands_set.append(i)

    return jsonify(brands_set)