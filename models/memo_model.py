import datetime as dt
from db import db_connect
class MemoModel:
    def add_memo(self,user_id,content, important=False): # 메모 추가
        content = content.strip()
        if not content:
            return
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = db_connect()
        cursor = conn.cursor()
        sql = "INSERT INTO memos (user_id, content, important, deleted, created_at) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_id, content, important, False, date))
        conn.commit()
        conn.close()
    def get_user_memos(self,user_id): # 메모 보기
        conn = db_connect()
        cursor = conn.cursor()
        sql = "SELECT id, user_id, content, important, deleted, created_at FROM memos WHERE user_id = %s and deleted = %s"
        cursor.execute(sql, (user_id, False))
        memos = cursor.fetchall()
        conn.close()
        return memos
    def delete_memo(self,memo_id, user_id): # 메모 삭제
        try:
            memo_id = int(memo_id)
        except ValueError:
            return
        conn = db_connect()
        cursor = conn.cursor()
        sql = "UPDATE memos SET deleted = %s WHERE id = %s and user_id = %s"
        cursor.execute(sql, (True, memo_id, user_id))
        conn.commit()
        conn.close()
        return
    def update_memo(self,memo_id,user_id,content): # 메모내용 수정
        try:
            memo_id = int(memo_id)
        except ValueError:
            return
        conn = db_connect()
        cursor = conn.cursor()
        sql = "UPDATE memos SET content = %s WHERE id = %s and user_id = %s"
        cursor.execute(sql,(content,memo_id,user_id))
        conn.commit()
        conn.close()
        return
    def set_important(self,memo_id, user_id): # 중요 표시/해제
        try:
            memo_id = int(memo_id)
        except ValueError:
            return
        conn = db_connect()
        cursor = conn.cursor()
        sql = "UPDATE memos SET important = NOT important WHERE id = %s and user_id = %s"
        cursor.execute(sql, (memo_id, user_id))
        conn.commit()
        conn.close()
        return
    def filter_by_keyword(self,memos,keyword): # 키워드로 필터링하기
        keyword = keyword.strip() if keyword else None
        filtered_memos = memos
        if not filtered_memos:
            return []
        if keyword is not None:
            filtered_memos  = [memo for memo in filtered_memos if keyword in memo["content"]]
        return filtered_memos
    def sort_memos(self,memos,sort_by, order): # 메모 정렬하기
        sorted_memos = memos
        if not sorted_memos:
            return []
        sorted_memos = sorted(memos, key=lambda x: x[sort_by], reverse=(order=="desc"))
        return sorted_memos
    def filter_by_important(self,memos,important): # 중요표시로 필터링하기
        important_memos = memos
        if not important_memos:
            return []
        if important is not None:
            important_memos = [memo for memo in important_memos if memo["important"]==important]
        return important_memos
    def get_final_memos(self,user_id, keyword="", sort_by="created_at", order="desc", important=None): # 최종적으로 보여줄 메모 가져오기
        memos = self.get_user_memos(user_id)
        memos = self.filter_by_keyword(memos, keyword)
        memos = self.filter_by_important(memos, important)
        memos = self.sort_memos(memos, sort_by, order)
        return memos
    def get_user_name(self,user_id):
        conn = db_connect()
        cursor = conn.cursor()
        sql = "SELECT name FROM users WHERE id = %s"
        cursor.execute(sql,user_id)
        name = cursor.fetchone()
        conn.close()
        if name:
            return name["name"]
