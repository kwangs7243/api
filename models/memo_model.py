import datetime as dt
from db import db_connect
class MemoModel:
    def add_memo(self,user_id,content, important=False): # 메모 추가
        content = content.strip()
        if not content:
            return
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = db_connect()
        cursor = conn.cursor()
        sql = "INSERT INTO memos (user_id, content, important, deleted, created_at) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_id, content, important, False, date))
        conn.commit()
        conn.close()
    def view_memos(self,user_id): # 메모 보기
        conn = db_connect()
        cursor = conn.cursor()
        sql = "SELECT id, user_id, content, important, deleted, created_at FROM memos WHERE user_id = %s and deleted = %s"
        cursor.execute(sql, (user_id, False))
        memos = cursor.fetchall()
        conn.close()
        if not memos:
            return []
        view_memos = []
        for memo in memos:
            memo = memo.copy()
            view_memos.append(memo)
        return view_memos
    def delete_memo(self,memo_id, user_id): # 메모 삭제
        try:
            memo_id = int(memo_id)
        except:
            return
        conn = db_connect()
        cursor = conn.cursor()
        sql = "UPDATE memos SET deleted = %s WHERE id = %s and user_id = %s"
        cursor.execute(sql, (True, memo_id, user_id))
        conn.commit()
        conn.close()
        return
    def set_important(self,memo_id, user_id): # 중요 표시/해제
        try:
            memo_id = int(memo_id)
        except:
            return
        conn = db_connect()
        cursor = conn.cursor()
        sql = "UPDATE memos SET important = NOT important WHERE id = %s and user_id = %s"
        cursor.execute(sql, (memo_id, user_id))
        conn.commit()
        conn.close()
        return
    def get_filtered_memos(self,memos,keyword): # 필터링된 메모 가져오기
        keyword = keyword.strip() if keyword else None
        filtered_memos = memos
        if not filtered_memos:
            return []
        if keyword is not None:
            filtered_memos  = [memo for memo in filtered_memos if keyword in memo["content"]]
        return filtered_memos
    def get_sorted_memos(self,memos,sort_by, sort_order): # 정렬 기준 설정
        sorted_memos = memos
        if not sorted_memos:
            return []
        if sort_by != "all":
            sorted_memos = sorted(memos, key=lambda x: x[sort_by], reverse=(sort_order=="desc"))
        return sorted_memos
    def get_important_memos(self,memos,important): # 중요 표시된 메모 가져오기
        important_memos = memos
        if not important_memos:
            return []
        if important:
            important_memos = [memo for memo in important_memos if memo["important"]]
        return important_memos
    def get_final_memos(self,user_id, keyword=None, sort_by="all", sort_order="asc", important=False): # 최종적으로 보여줄 메모 가져오기
        memos = self.view_memos(user_id)
        memos = self.get_filtered_memos(memos, keyword)
        memos = self.get_important_memos(memos, important)
        memos = self.get_sorted_memos(memos, sort_by, sort_order)
        return memos
