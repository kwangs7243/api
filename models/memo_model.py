from dbmanager import Dbmanager
class MemoModel:
    # db에 메모 추가
    def add_memo(self,dto):
        user_id = dto.user_id 
        content = dto.content
        important = dto.important
        
        with Dbmanager(commit=True) as cursor:
            sql = """
                    INSERT INTO memos 
                        (user_id, content, important, deleted) 
                        VALUES (%s, %s, %s, %s)
                    """
            cursor.execute(sql, (user_id, content, important, False))
    # db에서 메모목록 가져오기(화면상태 적용)
    def get_user_memos(self,dto): 
        user_id = dto.user_id
        keyword = dto.keyword
        important = dto.important
        sort_by = dto.sort_by
        order= dto.order

        where_clauses = ["user_id = %s", "deleted = %s"]
        params = [user_id, False]
       
        if keyword:
            where_clauses.append("content LIKE %s")
            params.append(f"%{keyword}%")

        if important is not None:
            where_clauses.append("important = %s")
            params.append(important)

        with Dbmanager() as cursor:
            sql = f"""
                    SELECT *
                        FROM memos
                        WHERE {" AND ".join(where_clauses)}
                        ORDER BY {sort_by} {order}, id {order}
                    """
            cursor.execute(sql, params)
            memos = cursor.fetchall()
        return memos
    # 메모 삭제 
    def delete_memo(self,dto):
        memo_id = dto.memo_id
        user_id = dto.user_id

        with Dbmanager(commit=True) as cursor:
            sql = """
                    UPDATE memos 
                        SET deleted = %s 
                        WHERE id = %s and user_id = %s"""
            cursor.execute(sql, (True, memo_id, user_id))
    # 메모내용 수정
    def update_memo(self,dto): 
        content = dto.content
        memo_id = dto.memo_id
        user_id = dto.user_id
        
        with Dbmanager(commit=True) as cursor:
            sql = """
                    UPDATE memos 
                        SET content = %s 
                        WHERE id = %s and user_id = %s
                    """
            cursor.execute(sql,(content,memo_id,user_id))
    # 중요 설정/해제
    def set_important(self,dto): 
        memo_id = dto.memo_id
        user_id = dto.user_id
        
        with Dbmanager(commit=True) as cursor:
            sql = """
                    UPDATE memos 
                        SET important = NOT important 
                        WHERE id = %s and user_id = %s
                    """
            cursor.execute(sql, (memo_id, user_id))

    def get_summary_memo(self, dto):
        with Dbmanager() as cursor:
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
            cursor.execute(sql, (dto.user_id, False))
            summary_memo = cursor.fetchone()

        return summary_memo
    
    def get_recent_memos(self, dto):
        with Dbmanager() as cursor:
            sql = """
                    SELECT important, content
                        FROM memos
                        WHERE user_id = %s AND deleted = %s
                        ORDER BY created_at desc, id asc
                        LIMIT 5
                    """
            cursor.execute(sql, (dto.user_id, False))
            recent_memos = cursor.fetchall()
        
        return recent_memos
