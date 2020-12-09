from flask import jsonify, request, session
from connection import connect_db


def product():
    product_set = []
    curr = connect_db().cursor()

    product_id = request.values.get('productId')
    categories_id = request.values.get('categories_id')
    brand_id = request.values.get('brand_id')
    price_min = request.values.get('pricemin')
    price_max = request.values.get('pricemax')
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
    elif brand_id is not None or categories_id is not None:
        sql += "WHERE "
        if brand_id is not None:
            sql += "b.brand_id = {} ".format(brand_id)
            if categories_id is not None:
                sql += " AND "
        if categories_id is not None:
            sql += "c.categories_id = {}".format(categories_id)
        if price_min is not None:
            sql += " AND product_price >= {} ".format(price_min)
        if price_max is not None:
            sql += " AND product_price <= {}".format(price_max)

    elif price_min is not None or price_max is not None:
        sql += "WHERE "
        if price_min is not None:
            sql += "product_price >= {}".format(price_min)
            if price_max is not None:
                sql += " AND "
            else:
                sql += " ORDER BY product_price"

        if price_max is not None:
            sql += "product_price <= {} ORDER BY product_price".format(price_max)

    curr.execute(sql)
    for i in curr:
        product_set.append(i)

    return jsonify(product_set)
