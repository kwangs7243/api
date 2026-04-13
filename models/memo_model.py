from db import db_connect
class MemoModel:
    # db에 메모 추가
    def add_memo(self,user_id,content, important=False): 
        content = content.strip()
        if not content:
            return
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                INSERT INTO memos 
                    (user_id, content, important, deleted) 
                    VALUES (%s, %s, %s, %s)
                """
        cursor.execute(sql, (user_id, content, important, False))
        conn.commit()
        conn.close()
    # db에서 메모목록 가져오기(화면상태 적용)
    def get_user_memos(self,user_id, keyword="", sort_by="created_at", order="desc", important=None): 
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

        conn = db_connect()
        cursor = conn.cursor()
        sql = f"""
                SELECT *
                    FROM memos
                    WHERE {" AND ".join(where_clauses)}
                    ORDER BY {sort_by} {order}, id {order}
                """
        cursor.execute(sql, params)
        memos = cursor.fetchall()
        conn.close()
        return memos
    # 메모 삭제 
    def delete_memo(self,memo_id, user_id):
        try:
            memo_id = int(memo_id)
        except ValueError:
            return
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                UPDATE memos 
                    SET deleted = %s 
                    WHERE id = %s and user_id = %s"""
        cursor.execute(sql, (True, memo_id, user_id))
        conn.commit()
        conn.close()
    # 메모내용 수정
    def update_memo(self,memo_id,user_id,content): 
        try:
            memo_id = int(memo_id)
        except ValueError:
            return
        
        content = content.strip()
        if content == "":
            return
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                UPDATE memos 
                    SET content = %s 
                    WHERE id = %s and user_id = %s
                """
        cursor.execute(sql,(content,memo_id,user_id))
        conn.commit()
        conn.close()
    # 중요 설정/해제
    def set_important(self,memo_id, user_id): 
        try:
            memo_id = int(memo_id)
        except ValueError:
            return
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                UPDATE memos 
                    SET important = NOT important 
                    WHERE id = %s and user_id = %s
                """
        cursor.execute(sql, (memo_id, user_id))
        conn.commit()
        conn.close()

    def get_summary_memo(self, user_id):
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                SELECT 
                    sum(
                        CASE WHEN important = TRUE THEN 1 ELSE 0 END) AS imp_t,
                    sum(
                        CASE WHEN important = FALSE THEN 1 ELSE 0 END) AS imp_f,
	                count(*) AS total
                    FROM memos
                    WHERE user_id = %s AND deleted = %s
                """
        cursor.execute(sql, (user_id, False))
        summary_memo = cursor.fetchone()
        conn.close()

        return summary_memo
    
    def get_recent_memos(self, user_id):
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                SELECT important, content
                    FROM memos
                    WHERE user_id = %s AND deleted = %s
                    ORDER BY created_at desc, id asc
                    LIMIT 5
                """
        cursor.execute(sql, (user_id, False))
        recent_memos = cursor.fetchall()
        conn.close()
        
        return recent_memos
