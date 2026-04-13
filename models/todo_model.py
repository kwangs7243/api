import datetime as dt
from db import db_connect
class TodoModel:
    # 할일 추가
    def add_todo(self,user_id,content):
        content = content.strip()
        if content == "":
            return
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                INSERT INTO todos
                    (user_id,content,completed,deleted)
                    VALUES (%s,%s,%s,%s)
                """
        cursor.execute(sql,(user_id,content,False,False))
        conn.commit()
        conn.close()
    # 할일목록 가져오기(화면상태 적용)
    def get_user_todos(self, user_id, keyword="", completed=False, sort_by="created_at", order="desc"): # 할일 보기
        where_clauses = ["user_id = %s", "deleted = %s"]
        params = [user_id, False]

        keyword = keyword.strip()
        if keyword:
            where_clauses.append("content LIKE %s")
            params.append(f"%{keyword}%")

        if completed is not None:
            where_clauses.append("completed = %s")
            params.append(completed)

        if sort_by not in ["created_at", "content", "completed"]:
            sort_by = "created_at"

        order = order.lower()
        if order not in ["asc", "desc"]:
            order = "desc"

        conn = db_connect()
        cursor = conn.cursor()
        sql = f"""
                SELECT *
                    FROM todos
                    WHERE {" AND ".join(where_clauses)}
                    ORDER BY {sort_by}, id {order}
                """
        cursor.execute(sql, params)
        todos = cursor.fetchall()
        conn.close()
        return todos
    # 할일 삭제
    def delete_todo(self,todo_id,user_id): 
        try:
            todo_id = int(todo_id)
        except ValueError:
            return
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                UPDATE todos
                    SET deleted = %s
                    WHERE id = %s AND user_id = %s
                """
        cursor.execute(sql,(True,todo_id,user_id))
        conn.commit()
        conn.close()
    # 내용 수정 
    def update_todo(self,todo_id,user_id,content): 
        content = content.strip()
        if content == "":
            return
        
        try:
            todo_id = int(todo_id)
        except ValueError:
            return
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                UPDATE todos
                    SET content = %s
                    WHERE id = %s AND user_id = %s
                """
        cursor.execute(sql,(content,todo_id,user_id))
        conn.commit()
        conn.close()
    # 완료여부 설정
    def set_completed(self,todo_id,user_id): 
        try:
            todo_id = int(todo_id)
        except ValueError:
            return
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                UPDATE todos
                    SET completed = NOT completed
                    WHERE id = %s AND user_id = %s
                """
        cursor.execute(sql,(todo_id,user_id))
        conn.commit()
        conn.close()
    
    def get_summary_todo(self, user_id):
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                SELECT 
                    sum(
                        CASE WHEN completed = TRUE THEN 1 ELSE 0 END) AS com_t,
                    sum(
                        CASE WHEN completed = FALSE THEN 1 ELSE 0 END) AS com_f,
	                count(*) AS total,
	                COALESCE(
	                        ROUND(
	   		                    sum(CASE WHEN completed = TRUE THEN 1 ELSE 0 END) * 100.0 / nullif(count(*),0), 2
                                ),0	   
	   		                ) AS com_per
                    FROM todos
                    WHERE user_id = %s AND deleted = %s
                """
        cursor.execute(sql, (user_id, False))
        summary_todo = cursor.fetchone()
        conn.close()

        return summary_todo
    
    def get_recent_todos(self, user_id):
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                SELECT completed, content
                    FROM todos
                    WHERE user_id = %s AND deleted = %s
                    ORDER BY created_at desc, id asc
                    LIMIT 5
                """
        cursor.execute(sql, (user_id, False))
        recent_todos = cursor.fetchall()
        conn.close()
        
        return recent_todos

