import pymysql
def db_connect():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="ezen123!",
        database="api",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn







