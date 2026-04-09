from flask import Blueprint , session, redirect,render_template,request
from models.memo_model import MemoModel
mm = MemoModel()
memo_bp = Blueprint("memo", __name__)

@memo_bp.route("/memo")
def main():
    if not "user_id"  in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    keyword = request.args.get("keyword" , "").strip()
    important_raw = request.args.get("important" , None)
    if important_raw == "1":
        important = True
    elif important_raw == "0":
        important = False
    else:
        important = None
    sort_by = request.args.get("sort_by" , "created_at")
    if not sort_by in ["created_at","content","important"]:
        sort_by = "created_at"
    order = request.args.get("order" , "desc")
    if not order in ["asc" , "desc"]:
        order = "desc"
    name = mm.get_user_name(user_id)
    memos = mm.get_final_memos(user_id, keyword=keyword, important=important, sort_by=sort_by, order=order, name=name)
    return render_template("memo.html",memos=memos,keyword = keyword,sort_by=sort_by,order=order,important=important)
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



    

