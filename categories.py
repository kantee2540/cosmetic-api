from flask import jsonify
from connection import connect_db


def categories():
    categories_set = []
    curr = connect_db().cursor()

    sql = "SELECT * FROM categories"

    curr.execute(sql)
    for i in curr:
        categories_set.append(i)

    return jsonify(categories_set)
