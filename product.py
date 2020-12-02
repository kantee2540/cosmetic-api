from flask import jsonify, request
from connection import connect_db


def product():
    product_set = []
    curr = connect_db().cursor()

    product_id = request.values.get('productId')
    limit = request.values.get('limit')
    keyword = request.values.get('keyword')
    sort = request.values.get('sort')

    sql = """SELECT * FROM product p
            JOIN product_brand b ON p.brand_id = b.brand_id 
            JOIN categories c ON p.categories_id = c.categories_id \n"""
    if product_id is not None:
        sql += "WHERE p.product_id={}".format(product_id)
    elif limit is not None:
        sql += "ORDER BY RAND() limit {}".format(limit)
    elif keyword is not None:
        sql += "WHERE p.product_name LIKE \"%{}%\"".format(keyword)
    elif sort is not None:
        sql += "ORDER BY p.View DESC limit 10"

    curr.execute(sql)
    for i in curr:
        product_set.append(i)

    return jsonify(product_set)
