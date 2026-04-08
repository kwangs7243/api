from flask import Blueprint , session
from models.memo_model import MemoModel
mm = MemoModel()
memo_bp = Blueprint("memo", __name__)

@memo_bp.route("/memo")
def main():
    if not "user_id"  in session:
        return
    user_id = session['user_id']
    memos = mm.get_filtered_memos(user_id)
@memo_bp.route("/memo/add")
def add():
    if not "user_id"  in session:
        return
    user_id = session['user_id']
    content = 'test'
    mm.add_memo(user_id,content)

    

