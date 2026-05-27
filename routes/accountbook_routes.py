from flask import Blueprint , session, redirect,render_template,request
from model.accountbook_model import AccountBookModel
from model.user_model import UserModel
from dtos.accountbook_dto import TransactionFilterDTO, TransactionCreateDTO, TransactionUpdateDTO, TransactionDeleteDTO
from service.formating import transactions_format, summary_format
am = AccountBookModel()
um = UserModel()
accountbook_bp = Blueprint("accountbook", __name__)

@accountbook_bp.route("/")
def main():
    if not "user_id" in session:
        return redirect("/sign/in")
    
    filter_dto = TransactionFilterDTO(
        user_id = session['user_id'],
        keyword = request.args.get("keyword"),
        category = request.args.get("category"),
        sort_by = request.args.get("sort_by" ),
        order = request.args.get("order")
        )

    name = um.get_user_name(filter_dto.user_id)
    transactions = transactions_format(am.get_user_transactions(filter_dto))
    
    
    transactions_summary = summary_format(am.get_summary_transaction(filter_dto))
   

    return render_template(
        "accountbook.html", 
        name=name, transactions=transactions, dto=filter_dto,
        transactions_summary = transactions_summary)

@accountbook_bp.route("/add", methods = ["POST"])
def add():
    if "user_id" not in session:
        return redirect("/sign/in")
    
  
    filter_dto = TransactionFilterDTO(
        user_id = session['user_id'],
        keyword = request.args.get("keyword"),
        category = request.args.get("category"),
        sort_by = request.args.get("sort_by" ),
        order = request.args.get("order")
        )
    
    create_dto = TransactionCreateDTO(
            user_id = session["user_id"],
            category = request.form.get("select_category"),
            amount = request.form.get("amount"),
            content = request.form.get("content")
            )
    am.add_transactions(create_dto)
    return redirect(f"/accountbook?&keyword={filter_dto.keyword}&category={filter_dto.category}&sort_by={filter_dto.sort_by}&order={filter_dto.order}")

@accountbook_bp.route("/update", methods=["POST"])
def update():
    if "user_id" not in session:
        return redirect("/sign/in")
    
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
        return redirect("/sign/in")
    
    user_id = session["user_id"]
    tt_id = request.form.get("tt_id")
    keyword = request.form.get("keyword")
    category = request.form.get("category")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")

    am.delete_transaction(tt_id, user_id)
    return redirect(f"/accountbook?&keyword={keyword}&category={category}&sort_by={sort_by}&order={order}")







