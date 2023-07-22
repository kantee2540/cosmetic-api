from flask import request
from connection import connect_db


def share_product():
    product_id = request.values.get('productId')

    curr = connect_db().cursor()
    sql = f"SELECT * FROM product p WHERE p.product_id = '{product_id}'"
    curr.execute(sql)
    data = curr.fetchone()

    return f"""
        <head>
            <meta http-equiv="refresh" content="3; url='cosmeticas://cosmetic?id={data['product_id']}'" />
            <title>{data['product_name']}</title>
        </head>
    """


def share_beauty_set():
    topic_id = request.values.get('topic_id')

    curr = connect_db().cursor()
    sql = f"SELECT * FROM today_topic t WHERE t.topic_id = '{topic_id}'"
    curr.execute(sql)
    data = curr.fetchone()

    return f"""
            <head>
                <meta http-equiv="refresh" content="3; url='cosmeticas://topic?id={data['topic_id']}'" />
                <title>{data['topic_name']}</title>
            </head>
        """
