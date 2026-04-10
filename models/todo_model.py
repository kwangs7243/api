import datetime as dt
from db import db_connect
class TodoModel:
    def add_todo(self,user_id,content): # 할일 추가
        content = content.strip()
        if content == "":
            return
        conn = db_connect()
        cursor = conn.cursor()
        sql = """INSERT INTO memos
                    (user_id,content,completed,deleted)
                    VALUES (%s,%s,%s,%s)"""
        cursor.execute(sql,(user_id,content,False,False))
        conn.commit()
        conn.close()
    def get_user_todos(self,user_id): # 할일 보기
        conn = db_connect()
        cursor = conn.cursor()
        sql = """SELECT *
                    FROM todos
                    WHERE user_id = %s AND deleted = %s"""
        cursor.execute(sql,(user_id,False))
        todos = cursor.fetchall()
        conn.close()
        return todos
    def delete_data(self,todo_id,user_id): # 할일 삭제
        try:
            todo_id = int(todo_id)
        except:
            return
        conn = db_connect()
        cursor = conn.cursor()
        sql = """UPDATE todos
                    SET deleted = %s
                    WHERE id = %s AND user_id = %s"""
        cursor.execute(sql,(True,todo_id,user_id))
        conn.commit()
        conn.close()
    def category_data(self,todos,):
        category_data = self.get_data()
        if not category_data:
            return  
        category = self.state["category"]
        if category != "all":
            category_data = [dic for dic in category_data if dic["category"] == category]
        return category_data
    def sorted_data(self):
        sorted_data = self.get_data()
        if not sorted_data:
            return
        column = self.state["sort_column"]
        direction = self.state["sort_direction"]
        if column is not None:
            if direction == "asc":
                sorted_data = sorted(sorted_data,key=lambda x:x[column],reverse=False)
            else:
                sorted_data = sorted(sorted_data,key=lambda x:x[column],reverse=True)
        return sorted_data
    def keyword_data(self):
        keyword_data = self.get_data()
        if not keyword_data:
            return
        keyword = self.state["keyword"]
        keyword_data = [dic for dic in keyword_data if keyword in dic["content"]]
        return keyword_data
    def set_completed(self,number):
        try:
            original_idx = int(number) - 1
        except:
            return
        self.todos[original_idx]["completed"] = True
        return
    def update_data(self,number,content):
        content = content.strip()
        if not content:
            return
        try:
            original_idx = int(number) - 1
        except:
            return
        self.todos[original_idx]["content"] = content
        return
    def view_data(self):
        view_data = self.get_data()
        view_data = self.keyword_data(view_data)
        if not view_data:
            return
        view_data = self.category_data(view_data)
        view_data = self.sorted_data(view_data)
        return view_data

