class TransactionFilterDTO:
    ALLOWED_CATEGORY = ("income", "expense")
    ALLOWED_SORT = ("created_at", "content", "amount", "category", "balance")
    ALLOWED_ORDER = ("asc", "desc")

    def __init__(self, user_id, keyword="", category=None, sort_by="created_at", order="desc"):
        self.user_id = int(user_id)
        self.keyword = (keyword or "").strip()
        self.category = category if category in self.ALLOWED_CATEGORY else None
        self.sort_by = sort_by if sort_by in self.ALLOWED_SORT else "created_at"

        order = (order or "desc").lower()
        self.order = order if order in self.ALLOWED_ORDER else "desc"

class TransactionCreateDTO:
    def __init__(self, user_id, category, amount, content):
        self.user_id = user_id
        self.category = category
        self.amount = amount
        self.content = content

class TransactionUpdateDTO:
    def __init__(self, user_id, transaction_id, category, amount, content):
        self.user_id = user_id
        self.transaction_id = transaction_id
        self.category = category
        self.amount = amount
        self.content = content


class TransactionDeleteDTO:
    def __init__(self, user_id, transaction_id):
        self.user_id = user_id
        self.transaction_id = transaction_id