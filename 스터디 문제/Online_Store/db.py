import MySQLdb


def get_connect():
    return MySQLdb.connect(
        host="localhost",
        user="apple",
        password="1111",
        db="online_store",
        charset="utf8",
    )
