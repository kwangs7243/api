import pymysql
class Dbmanager:
    def __init__(self,commit=False):
        self.commit = commit
    def __enter__(self):
        self.conn = pymysql.connect(
                    host="localhost",
                    user="root",
                    password="ezen123!",
                    database="api",
                    charset="utf8",
                    cursorclass=pymysql.cursors.DictCursor
                    )
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type:
                self.conn.rollback()
            elif self.commit:
                self.conn.commit()
        finally:
            self.cursor.close()
            self.conn.close()



