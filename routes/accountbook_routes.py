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
    if  category not in ["income", "expense"]:
        category = None

    sort_by = request.args.get("sort_by" , "created_at")
    if  sort_by not in ["created_at","content","amount", "category", "balance"]:
        sort_by = "created_at"

    order = request.args.get("order" , "desc")
    order = order.lower()
    if  order not in ["asc" , "desc"]:
        order = "desc"

    name = um.get_user_name(user_id)
    transactions = am.get_user_transactions(user_id, keyword=keyword, category=category, sort_by=sort_by, order=order)
    for transaction in transactions:
        transaction["format_amount"] = f"{transaction['amount']:,} 원"
        transaction["format_balance"] = f"{transaction['balance']:,} 원"
    
    transactions_summary = am.get_transactions_summary(user_id)
    total_balance = f"{transactions_summary['total_balance']:,} 원"
    income_sum = f"{transactions_summary['income_sum']:,} 원"
    expense_sum = f"{transactions_summary['expense_sum']:,} 원"

    return render_template(
        "accountbook.html", 
        name=name, transactions=transactions, keyword=keyword, 
        category=category, sort_by=sort_by, order=order,
        total_balance=total_balance, income_sum=income_sum, expense_sum=expense_sum)

@accountbook_bp.route("/add", methods = ["POST"])
def add():
    if "user_id" not in session:
        return redirect("/sign_in")
    
    user_id = session["user_id"]
    keyword = request.form.get("keyword")
    category = request.form.get("category")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")

    select_category = request.form.get("select_category")
    if select_category not in ["income", "expense"]:
        return redirect(f"/accountbook?&keyword={keyword}&category={category}&sort_by={sort_by}&order={order}")

    amount = request.form.get("amount")
    try:
        amount = int(amount)
    except ValueError:
        return redirect(f"/accountbook?&keyword={keyword}&category={category}&sort_by={sort_by}&order={order}")
    content = request.form.get("content")

    am.add_transactions(user_id,select_category,amount,content)
    return redirect(f"/accountbook?&keyword={keyword}&category={category}&sort_by={sort_by}&order={order}")

@accountbook_bp.route("/update", methods=["POST"])
def update():
    if "user_id" not in session:
        return redirect("/sign_in")
    
    user_id = session["user_id"]
    tt_id = request.form.get("tt_id")
    keyword = request.form.get("keyword")
    category = request.form.get("category")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")

    update_category = request.form.get("update_category")
    if update_category not in ["income", "expense"]:
        return redirect(f"/accountbook?&keyword={keyword}&category={category}&sort_by={sort_by}&order={order}")

    update_amount = request.form.get("update_amount")
    try:
        update_amount = int(update_amount)
    except ValueError:
        return redirect(f"/accountbook?&keyword={keyword}&category={category}&sort_by={sort_by}&order={order}")
    
    update_content = request.form.get("update_content").strip()
    if not update_content:
        return redirect(f"/accountbook?&keyword={keyword}&category={category}&sort_by={sort_by}&order={order}")

    am.update_transactions(tt_id, user_id, update_content, update_category, update_amount)
    return redirect(f"/accountbook?&keyword={keyword}&category={category}&sort_by={sort_by}&order={order}")

@accountbook_bp.route("/delete", methods=["POST"])
def delete():
    if "user_id" not in session:
        return redirect("/sign_in")
    
    user_id = session["user_id"]
    tt_id = request.form.get("tt_id")
    keyword = request.form.get("keyword")
    category = request.form.get("category")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")

    am.delete_transaction(tt_id, user_id)
    return redirect(f"/accountbook?&keyword={keyword}&category={category}&sort_by={sort_by}&order={order}")







