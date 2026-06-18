import MySQLdb


def get_connection():
    return MySQLdb.connect(
        host="localhost",
        user="apple",
        password="1111",
        db="study_manager",
        charset="utf8",
    )
