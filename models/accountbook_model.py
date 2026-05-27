from dbmanager import Dbmanager
class AccountBookModel:
    # 내용 추가
    def add_transactions(self,dto):
        user_id = dto.user_id
        category = dto.category
        amount = dto.amount
        content = dto.content

        with Dbmanager(commit=True) as cursor:
            sql = """
                    INSERT INTO accountbook
                        (user_id, category, amount, content, deleted)
                        VALUES(%s, %s, %s, %s, %s)
                    """
            cursor.execute(sql,(user_id, category, amount, content, False))
    # 가계부 내역 가져오기
    def get_user_transactions(self,dto):
        user_id = dto.user_id
        keyword = dto.keyword
        category = dto.category
        sort_by = dto.sort_by
        order = dto.order

        where_clauses = []
        params = [user_id, False]

        if keyword:
            where_clauses.append("content LIKE %s")
            params.append(f"%{keyword}%")

        if category in ("income", "expense"):
            where_clauses.append("category = %s")
            params.append(category)
        
        outer_where = ""
        if where_clauses:
            outer_where = "WHERE " + " AND ".join(where_clauses)
        
        with Dbmanager() as cursor:
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
        return transactions
    # 내역 삭제하기
    def delete_transaction(self,dto):
        user_id = dto.user_id
        tt_id = dto.tt_id
        with Dbmanager(commit=True) as cursor:
            sql = """
                    UPDATE accountbook
                        SET deleted = %s
                        WHERE user_id = %s AND id = %s
                    """
            cursor.execute(sql, (True, user_id, tt_id))
    # 내역 수정하기
    def update_transactions(self, dto):
        content = dto.content
        category = dto.category
        amount = dto.amount
        user_id = dto.user_id
        tt_id = dto.tt_id
        set_clauses = []
        params = []

        if content:
            set_clauses.append("content = %s")
            params.append(content)

        if category:
            set_clauses.append("category = %s")
            params.append(category)
        
        if amount:
            set_clauses.append("amount = %s")
            params.append(amount)
        
        if not set_clauses:
            return
        
        with Dbmanager(commit=True) as cursor:
            sql = f"""
                    UPDATE accountbook
                        SET {",".join(set_clauses)}
                        WHERE user_id = %s AND id = %s
                    """
            cursor.execute(sql, params + [user_id, tt_id])

    def get_summary_transaction(self,dto):
        user_id = dto.user_id
        with Dbmanager() as cursor:
            sql = """
                    SELECT (income_sum - expense_sum) AS total_balance , income_sum, expense_sum
                        FROM(
                            SELECT sum(CASE WHEN category = 'income' THEN amount ELSE 0 END ) AS income_sum,
                                    sum(CASE WHEN category = 'expense' THEN amount ELSE 0 END ) AS expense_sum                                       
                                    FROM accountbook
                                    WHERE user_id = %s AND deleted = %s ) AS sub
                    """
            cursor.execute(sql, (user_id, False))
            summary_transactions = cursor.fetchone()
        return summary_transactions
    
    def get_recent_transactions(self, user_id):
        with Dbmanager() as cursor:
            sql = """
                    SELECT category, content, amount
                        FROM accountbook
                        WHERE user_id = %s AND deleted = %s
                        ORDER BY created_at desc, id asc
                        LIMIT 5
                    """
            cursor.execute(sql, (user_id, False))
            recent_transactions = cursor.fetchall()
        return recent_transactions













    


