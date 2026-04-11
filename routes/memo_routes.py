from flask import Blueprint , session, redirect,render_template,request
from models.memo_model import MemoModel
from models.user_model import UserModel
mm = MemoModel()
um = UserModel()
memo_bp = Blueprint("memo", __name__)
@memo_bp.route("/")
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
    order = order.lower()
    if not order in ["asc" , "desc"]:
        order = "desc"
    name = um.get_user_name(user_id)
    memos = mm.get_user_memos(user_id, keyword=keyword, important=important, sort_by=sort_by, order=order)
    return render_template(
        "memo.html",
        memos=memos,keyword = keyword,
        sort_by=sort_by,order=order,
        important=important,name=name)
@memo_bp.route("/add", methods=["POST"])
def add():
    if not "user_id"  in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    keyword = request.form.get("keyword","")
    content = request.form.get("content")
    important = request.form.get("important")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")
    mm.add_memo(user_id,content)
    return redirect(f"/memo?&keyword={keyword}&important={important}&sort_by={sort_by}&order={order}")
@memo_bp.route("/delete",methods=["POST"])
def delete():
    if not "user_id"  in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    memo_id = request.form.get("memo_id")
    keyword = request.form.get("keyword","")
    important = request.form.get("important")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")
    mm.delete_memo(memo_id,user_id)
    return redirect(f"/memo?&keyword={keyword}&important={important}&sort_by={sort_by}&order={order}")

@memo_bp.route("/important",methods=["POST"])
def important():
    if not "user_id"  in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    memo_id = request.form.get("memo_id")
    keyword = request.form.get("keyword","")
    important = request.form.get("important")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")
    mm.set_important(memo_id,user_id)
    return redirect(f"/memo?&keyword={keyword}&important={important}&sort_by={sort_by}&order={order}")

@memo_bp.route("/update", methods=["POST"])
def update():
    if not "user_id"  in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    memo_id = request.form.get("memo_id")
    keyword = request.form.get("keyword","")
    content = request.form.get("update").strip()
    important = request.form.get("important")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")
    mm.update_memo(user_id=user_id,memo_id=memo_id,content=content)
    return redirect(f"/memo?&keyword={keyword}&important={important}&sort_by={sort_by}&order={order}")



    

