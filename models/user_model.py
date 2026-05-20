from dbmanager import Dbmanager
class UserModel:
    def check_id_duplication(self, login_id):  #  아이디 중복 체크
        with Dbmanager() as cursor:
            sql = "SELECT login_id From users WHERE login_id = %s"
            cursor.execute(sql, (login_id,))
            result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    def sign_up(self, login_id, passwd, name): # 회원가입
        with Dbmanager(commit=True) as cursor:
            sql = "INSERT INTO users (login_id, passwd, name) VALUES (%s, %s, %s)"
            cursor.execute(sql, (login_id, passwd, name))
    def sign_in(self, login_id, passwd): # 로그인
        with Dbmanager() as cursor:
            sql = "SELECT id,login_id FROM users WHERE login_id = %s AND passwd = %s"
            cursor.execute(sql, (login_id, passwd))
            result = cursor.fetchone()
        user_id = result["id"] if result else None
        return user_id
    def get_user_name(self,user_id): # 유저이름 가져오기
        with Dbmanager() as cursor:
            sql = "SELECT name FROM users WHERE id = %s"
            cursor.execute(sql,(user_id,))
            name = cursor.fetchone()
        if name:
            return name["name"]
