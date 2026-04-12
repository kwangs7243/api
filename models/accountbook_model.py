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
    # 가계부 내역 가져오기
    def get_user_transactions(self, user_id, keyword="", category=None, sort_by="created_at", order="desc"):
        where_clauses = []
        params = [user_id, False]

        keyword = keyword.strip()
        if keyword:
            where_clauses.append("content LIKE %s")
            params.append(f"%{keyword}%")

        if category is not None:
            where_clauses.append("category = %s")
            params.append(category)
        
        if sort_by not in ["created_at", "content", "amount", "balance"]:
            sort_by = "created_at"
        
        order = order.lower()
        if order not in ["asc", "desc"]:
            order = "desc"

        outer_where = ""
        if where_clauses:
            outer_where = "WHERE" + " AND ".join(where_clauses)
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = f"""
                SELECT id, user_id, category, amount, content, balance, created_at
                    FROM (
                        SELECT id, user_id, category, amount, content, deleted, created_at,
                        sum(CASE WHEN category = 'income' THEN amount
                                WHEN category = 'expense' THEN -amount
                                ELSE 0
                            END
                            ) OVER (ORDER BY created_at ASC, id ASC) AS balance
                    FROM accountbook
                    WHERE user_id = %s AND deleted = %s
                    ) AS sub
                    {outer_where}
                    ORDER BY {sort_by} {order} , id {order}
                """
        cursor.execute(sql, params)
        transactions = cursor.fetchall()
        conn.close()
        return transactions














    


