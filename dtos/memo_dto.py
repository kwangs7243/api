ALLOWED_SORT = ("created_at", "content", "important")
ALLOWED_ORDER = ("asc", "desc")

class MemoFilterDTO:
    def __init__(self, user_id, keyword="", sort_by="created_at", order="desc", important=None):
        self.user_id = int(user_id)
        self.keyword = (keyword or "").strip()
        self.sort_by = sort_by if sort_by in ALLOWED_SORT else "created_at"

        if important == "1":
            self.important_query = "1"
            self.important = True
        elif important == "0":
            self.important_query = "0"
            self.important = False
        else:
            self.important_query = ""
            self.important = None

        order = (order or "desc").lower()
        self.order = order if order in ALLOWED_ORDER else "desc"

class MemoCreateDTO:
    def __init__(self, user_id,content, important=False):
        self.user_id = int(user_id)
        self.content = content
        self.important = important

class MemoDeleteDTO:
    def __init__(self, memo_id, user_id):
        self.memo_id = int(memo_id)
        self.user_id = int(user_id)

class MemoUpdateDTO:
    def __init__(self, memo_id, user_id, content=""):
        self.memo_id = int(memo_id)
        self.user_id = int(user_id)
        self.content = content