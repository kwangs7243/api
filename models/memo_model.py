import datetime as dt
from db import db_connect
class MemoModel:
    def add_memo(self,user_id,content, important=False): # 메모 추가
        content = content.strip()
        if not content:
            return
        conn = db_connect()
        cursor = conn.cursor()
        sql = "INSERT INTO memos (user_id, content, important, deleted) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (user_id, content, important, False))
        conn.commit()
        conn.close()
    def get_user_memos(self,user_id, keyword="", sort_by="created_at", order="desc", important=None): # 메모 보기
        conn = db_connect()
        cursor = conn.cursor()
        where_clauses = ["user_id = %s", "deleted = %s"]
        params = [user_id, False]
        keyword = keyword.strip()
        if keyword:
            where_clauses.append("content LIKE %s")
            params.append(f"%{keyword}%")
        if important is not None:
            where_clauses.append("important = %s")
            params.append(important)
        if sort_by not in ["created_at", "content", "important"]:
            sort_by = "created_at"
        order = order.lower()
        if order not in ["asc", "desc"]:
            order = "desc"
        sql = f"""
            SELECT *
                FROM memos
                WHERE {" AND ".join(where_clauses)}
                ORDER BY {sort_by} {order}
                """
        cursor.execute(sql, params)
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
        content = content.strip()
        if content == "":
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