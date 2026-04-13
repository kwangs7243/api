from flask import Blueprint , session, redirect,render_template,request
from models.accountbook_model import AccountBookModel
from models.user_model import UserModel
am = AccountBookModel()
um = UserModel()
accountbook_bp = Blueprint("accountbook", __name__)

@accountbook_bp.route("/")
def main():
    if not "user_id" in session:
        return redirect("/sign_in")
    user_id = session['user_id']

    keyword = request.args.get("keyword", "").strip()

    category = request.args.get("category", None)
    if not category in ["income", "expense"]:
        category = None

    sort_by = request.args.get("sort_by" , "created_at")
    if not sort_by in ["created_at","content","amount", "category"]:
        sort_by = "created_at"

    order = request.args.get("order" , "desc")
    order = order.lower()
    if not order in ["asc" , "desc"]:
        order = "desc"

    name = um.get_user_name(user_id)
    transactions = am.get_user_transactions(user_id, keyword=keyword, category=category, sort_by=sort_by, order=order)

    return render_template(
        "accountbook.html", 
        name=name, transactions=transactions, keyword=keyword, 
        category=category, sort_by=sort_by, order=order)

@accountbook_bp.route("/add", methods = ["POST"])
def add():
    if not "user_id" in session:
        return redirect("/sign_in")
    
    user_id = session["user_id"]
    keyword = request.form.get("keyword")
    category = request.form.get("category")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")

    select_category = request.form.get("select_category")
    if not select_category in ["income", "expense"]:
        return redirect("/accountbook")

    amount = request.form.get("amount")
    try:
        amount = int(amount)
    except ValueError:
        return redirect("/accountbook")
    content = request.form.get("content").strip()

    am.add_transactions(user_id,select_category,amount,content)
    return redirect(f"/accountbook?&keyword={keyword}&category{category}&sort_by={sort_by}&order={order}")
