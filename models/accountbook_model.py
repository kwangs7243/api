from db import db_connect
class AccountBookModel:
    # 내용 추가
    def add_AB(self,user_id,category,amount,content):
        if category not in ["income","expensd"]:
            return
        
        try:
            amount = int(amount)
        except ValueError:
            return
        
        content = content.strip()
        if not content:
            return
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                INSERT INTO accountbook
                    (user_id, category, amount, content, deleted)
                    VALUES(%s, %s, %s, %s, %s)
                """
        cursor.execute(sql(user_id, category, amount, content, False))
        conn.commit()
        conn.close()
    # 가계부 목록 가져오기
    def get_user_AB(self, user_id, keyword="", category=None, sort_by="created_at", order="desc"):
        where_clauses = ["user_id = %s", "deleted = %s"]
        params = [user_id, False]

        keyword = keyword.strip()
        if keyword:
            where_clauses.append("content LIKE %s")
            params.append(f"%{keyword}%")

        if category is not None:
            where_clauses.append("category = %s")
            params.append(category)
        
        if sort_by not in ["created_at", "content", "amount"]:
            sort_by = "created_dy"
        
        order = order.lower()
        if order not in ["asc", "desc"]:
            order = "desc"
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = f"""
                SELECT *
                    FROM accountbook
                    WHERE {" AND ".join(where_clauses)}
                    ORDER BY {sort_by}, id {order}
                """
        cursor.execute(sql, params)
        accountbook = cursor.fetchall()
        conn.close()
        return accountbook
    
    













    


