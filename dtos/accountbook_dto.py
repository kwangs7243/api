ALLOWED_CATEGORY = ("income", "expense")
ALLOWED_SORT = ("created_at", "content", "amount", "category", "balance")
ALLOWED_ORDER = ("asc", "desc")
class TransactionFilterDTO:
    def __init__(self, user_id, keyword="", category=None, sort_by="created_at", order="desc"):
        self.user_id = int(user_id)
        self.keyword = (keyword or "").strip()
        self.category = category if category in ALLOWED_CATEGORY else None
        self.sort_by = sort_by if sort_by in ALLOWED_SORT else "created_at"

        order = (order or "desc").lower()
        self.order = order if order in ALLOWED_ORDER else "desc"

class TransactionCreateDTO:
    def __init__(self, user_id, category, amount, content):
        self.user_id = int(user_id)
        self.category = category if category in ALLOWED_CATEGORY else None
        try:
            self.amount = int(amount)
        except ValueError as e:
            raise "금액입력오류" from e
        self.content = content

class TransactionUpdateDTO:
    def __init__(self, user_id, tt_id, category, amount, content):
        self.user_id = int(user_id)
        self.tt_id = int(tt_id)
        self.category = category if category in ALLOWED_CATEGORY else None
        try:
            self.amount = int(amount)
        except ValueError as e:
            raise "금액입력오류" from e
        self.content = content


class TransactionDeleteDTO:
    def __init__(self, user_id, tt_id):
        self.user_id = int(user_id)
        self.tt_id = int(tt_id)