import pymysql
import yaml


def connect_db():

    cfg = {}
    with open('config.yaml') as config_file:
        cfg = yaml.load(config_file, Loader=yaml.FullLoader)['database']

    connection = pymysql.connect(host=cfg['host'],
                                 user=cfg['user'],
                                 password=cfg['password'],
                                 db=cfg['db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)

    return connection
