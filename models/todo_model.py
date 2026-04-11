import datetime as dt
from db import db_connect
class TodoModel:
    def add_todo(self,user_id,content): # 할일 추가
        content = content.strip()
        if content == "":
            return
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
            INSERT INTO memos
                (user_id,content,completed,deleted)
                VALUES (%s,%s,%s,%s)
            """
        cursor.execute(sql,(user_id,content,False,False))
        conn.commit()
        conn.close()
    def get_user_todos(self, user_id, keyword="", completed=False, sort_by="created_at", order="desc"): # 할일 보기
        conn = db_connect()
        cursor = conn.cursor()
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
        sql = f"""
            SELECT *
                FROM todos
                WHERE {" AND ".join(where_clauses)}
                ORDER BY {sort_by} {order}
            """
        cursor.execute(sql, params)
        todos = cursor.fetchall()
        conn.close()
        return todos
    def delete_todo(self,todo_id,user_id): # 할일 삭제
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
    def update_todo(self,todo_id,user_id,content): # 내용 수정 
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
    def set_completed(self,todo_id,user_id): # 완료여부 설정
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

