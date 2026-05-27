from flask import Blueprint , session, redirect,render_template,request,url_for
from models.accountbook_model import AccountBookModel
from models.user_model import UserModel
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

    user_name = um.get_user_name(filter_dto)

    transactions = transactions_format(am.get_user_transactions(filter_dto))
    
    transactions_summary = summary_format(am.get_summary_transaction(filter_dto))
   

    return render_template(
        "accountbook.html", 
        user_name=user_name, transactions=transactions, dto=filter_dto,
        transactions_summary = transactions_summary)

@accountbook_bp.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/sign/in")

    filter_dto = TransactionFilterDTO(
        user_id=session["user_id"],
        keyword=request.form.get("keyword"),
        category=request.form.get("category"),
        sort_by=request.form.get("sort_by"),
        order=request.form.get("order")
    )

    create_dto = TransactionCreateDTO(
        user_id=session["user_id"],
        category=request.form.get("select_category"),
        amount=request.form.get("amount"),
        content=request.form.get("content")
    )

    am.add_transactions(create_dto)

    return redirect(
        url_for(
            "accountbook.main",
            keyword=filter_dto.keyword,
            category=filter_dto.category,
            sort_by=filter_dto.sort_by,
            order=filter_dto.order
        )
    )
@accountbook_bp.route("/update", methods=["POST"])
def update():
    if "user_id" not in session:
        return redirect("/sign/in")
    
    filter_dto = TransactionFilterDTO(
        user_id=session["user_id"],
        keyword=request.form.get("keyword"),
        category=request.form.get("category"),
        sort_by=request.form.get("sort_by"),
        order=request.form.get("order")
    )
   
   
    update_dto = TransactionUpdateDTO(
        user_id=session["user_id"],
        tt_id = request.form.get("tt_id"),
        category = request.form.get("update_category"),
        amount = request.form.get("update_amount"),
        content = request.form.get("update_content")
    )

    am.update_transactions(update_dto)

    return redirect(
        url_for(
            "accountbook.main",
            keyword=filter_dto.keyword,
            category=filter_dto.category,
            sort_by=filter_dto.sort_by,
            order=filter_dto.order
        )
    )

@accountbook_bp.route("/delete", methods=["POST"])
def delete():
    if "user_id" not in session:
        return redirect("/sign/in")
    filter_dto = TransactionFilterDTO(
        user_id=session["user_id"],
        keyword=request.form.get("keyword"),
        category=request.form.get("category"),
        sort_by=request.form.get("sort_by"),
        order=request.form.get("order")
    )
    delete_dto = TransactionDeleteDTO(
        user_id=session["user_id"],
        tt_id = request.form.get("tt_id")
    )
    
    am.delete_transaction(delete_dto)

    return redirect(
    url_for(
        "accountbook.main",
        keyword=filter_dto.keyword,
        category=filter_dto.category,
        sort_by=filter_dto.sort_by,
        order=filter_dto.order
        )
    )







