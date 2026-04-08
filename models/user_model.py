from db import db_connect
class UserModel:
    def check_id_duplication(self, login_id):  #  아이디 중복 체크
        conn = db_connect()
        cursor = conn.cursor()
        sql = "SELECT login_id From users WHERE login_id = %s"
        cursor.execute(sql, (login_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return True
        else:
            return False
    def sign_up(self, login_id, passwd, name): # 회원가입
        conn = db_connect()
        cursor = conn.cursor()
        sql = "INSERT INTO users (login_id, passwd, name) VALUES (%s, %s, %s)"
        cursor.execute(sql, (login_id, passwd, name))
        conn.commit()
        conn.close()
    def sign_in(self, login_id, passwd): # 로그인
        conn = db_connect()
        cursor = conn.cursor()
        sql = "SELECT id,login_id FROM users WHERE login_id = %s AND passwd = %s"
        cursor.execute(sql, (login_id, passwd))
        result = cursor.fetchone()
        conn.close()
        user_id = result["id"] if result else None
        return user_id
