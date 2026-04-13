from db import db_connect
class AccountBookModel:
    # 내용 추가
    def add_transactions(self,user_id,category,amount,content):
        if not category in ["income","expense"]:
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
        cursor.execute(sql,(user_id, category, amount, content, False))
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

        if category in ("income", "expense"):
            where_clauses.append("category = %s")
            params.append(category)
        
        if sort_by not in ["created_at", "content", "amount", "balance", "category"]:
            sort_by = "created_at"
        
        order = order.lower()
        if order not in ["asc", "desc"]:
            order = "desc"

        outer_where = ""
        if where_clauses:
            outer_where = "WHERE " + " AND ".join(where_clauses)
        
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
    # 내역 삭제하기
    def delete_transaction(self,tt_id,user_id):
        try:
            tt_id = int(tt_id)
        except ValueError:
            return
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                UPDATE accountbook
                    SET deleted = %s
                    WHERE user_id = %s AND id = %s
                """
        cursor.execute(sql, (True, user_id, tt_id))
        conn.commit()
        conn.close()
    # 내역 수정하기
    def update_transactions(self, tt_id, user_id, content, category, amount):
        try:
            tt_id = int(tt_id)
        except ValueError:
            return
        
        set_clauses = []
        params = []
        
        content = content.strip()
        set_clauses.append("content = %s")
        params.append(content)
        
        
        if category in ["income", "expense"]:
            set_clauses.append("category = %s")
            params.append(category)
        
        
        try:
            amount = int(amount)
        except ValueError:
            return
        set_clauses.append("amount = %s")
        params.append(amount)
        
        if not set_clauses:
            return
        
        conn = db_connect()
        cursor = conn.cursor()
        sql = f"""
                UPDATE accountbook
                    SET {",".join(set_clauses)}
                    WHERE user_id = %s AND id = %s
                """
        cursor.execute(sql, params + [user_id, tt_id])
        conn.commit()
        conn.close()

    def get_transactions_summary(self,user_id):
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                SELECT (income_sum - expense_sum) AS total_balance , income_sum, expense_sum
	                FROM(
                        SELECT sum(CASE WHEN category = 'income' THEN amount ELSE 0 END ) AS income_sum,
                                sum(CASE WHEN category = 'expense' THEN amount ELSE 0 END ) AS expense_sum                                       
                                FROM accountbook
                                WHERE user_id = %s AND deleted = %s ) AS sub
                """
        cursor.execute(sql, (user_id, False))
        transactions_summary = cursor.fetchone()
        conn.close()
        return transactions_summary
    
    def get_recent_transactions(user_id):
        conn = db_connect()
        cursor = conn.cursor()
        sql = """
                SELECT category, content, amount
                    FROM accountbook
                    WHERE user_id = %s AND deleted = %s
                    ORDER BY created_at desc, id asc
                    LIMIT 5
                """
        cursor.execute(sql, (user_id, False))
        recent_transactions = cursor.fetchall()
        conn.close()
        return recent_transactions













    


