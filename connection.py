import pymysql


def connect_db():
    connection = pymysql.connect(host="localhost",
                                 user="root",
                                 password="",
                                 db="cosmetic-mobile",
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)

    return connection
