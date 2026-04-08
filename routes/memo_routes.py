from flask import Blueprint , session, redirect,render_template,request
from models.memo_model import MemoModel
mm = MemoModel()
memo_bp = Blueprint("memo", __name__)

@memo_bp.route("/memo")
def main():
    if not "user_id"  in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    memos = mm.view_memos(user_id)
    return render_template("memo.html",memos=memos)
@memo_bp.route("/memo/add", methods=["POST"])
def add():
    if not "user_id"  in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    content = request.form.get("content")
    mm.add_memo(user_id,content)
    return redirect("/memo")
@memo_bp.route("/memo/delete",methods=["POST"])
def delete():
    if not "user_id"  in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    memo_id = request.form.get("memo_id")
    mm.delete_memo(memo_id,user_id)
    return redirect("/memo")
@memo_bp.route("/memo/important",methods=["POST"])
def important():
    if not "user_id"  in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    memo_id = request.form.get("memo_id")
    mm.set_important(memo_id,user_id)
    return redirect("/memo")



    

