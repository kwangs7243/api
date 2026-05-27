from flask import Blueprint , session, redirect,render_template,request,url_for
from models.memo_model import MemoModel
from models.user_model import UserModel
from dtos.memo_dto import MemoCreateDTO,MemoDeleteDTO,MemoFilterDTO,MemoUpdateDTO
mm = MemoModel()
um = UserModel()
memo_bp = Blueprint("memo", __name__)
@memo_bp.route("/")
def main():
    if "user_id" not in session:
        return redirect("/sign/in")

    filter_dto = MemoFilterDTO(
        user_id = session['user_id'],
        keyword = request.args.get("keyword"),
        important = request.args.get("important"),
        sort_by = request.args.get("sort_by"),
        order = request.args.get("order")
    )
    user_name = um.get_user_name(filter_dto)
    memos = mm.get_user_memos(filter_dto)
    return render_template(
        "memo.html",
        memos = memos, 
        dto = filter_dto, 
        user_name = user_name
        )

@memo_bp.route("/add", methods=["POST"])
def add():
    if  "user_id" not in session:
        return redirect("/sign/in")
    filter_dto = MemoFilterDTO(
        user_id = session['user_id'],
        keyword = request.form.get("keyword"),
        important = request.form.get("important"),
        sort_by = request.form.get("sort_by"),
        order = request.form.get("order")
    )
    create_dto = MemoCreateDTO(
        user_id = session['user_id'],
        content = request.form.get("content")
    )
    
    mm.add_memo(create_dto)

    return redirect(
        url_for(
            "memo.main",
            keyword = filter_dto.keyword,
            important = filter_dto.important_query,
            sort_by = filter_dto.sort_by,
            order = filter_dto.order
        )
    )

@memo_bp.route("/delete",methods=["POST"])
def delete():
    if  "user_id" not in session:
        return redirect("/sign/in")
    filter_dto = MemoFilterDTO(
        user_id = session['user_id'],
        keyword = request.form.get("keyword"),
        important = request.form.get("important"),
        sort_by = request.form.get("sort_by"),
        order = request.form.get("order")
    )
    delete_dto = MemoDeleteDTO(
        memo_id = request.form.get("memo_id"),
        user_id = session['user_id']
    )

    mm.delete_memo(delete_dto)

    return redirect(
        url_for(
            "memo.main",
            keyword = filter_dto.keyword,
            important = filter_dto.important_query,
            sort_by = filter_dto.sort_by,
            order = filter_dto.order
        )
    )

@memo_bp.route("/important",methods=["POST"])
def important():
    if  "user_id" not in session:
        return redirect("/sign/in")
    filter_dto = MemoFilterDTO(
        user_id = session['user_id'],
        keyword = request.form.get("keyword"),
        important = request.form.get("important"),
        sort_by = request.form.get("sort_by"),
        order = request.form.get("order")
    )
    update_dto = MemoUpdateDTO(
        memo_id = request.form.get("memo_id"),
        user_id = session['user_id']
    )
    
    mm.set_important(update_dto)

    return redirect(
        url_for(
            "memo.main",
            keyword = filter_dto.keyword,
            important = filter_dto.important_query,
            sort_by = filter_dto.sort_by,
            order = filter_dto.order
        )
    )

@memo_bp.route("/update", methods=["POST"])
def update():
    if  "user_id" not in session:
        return redirect("/sign/in")
    filter_dto = MemoFilterDTO(
        user_id = session['user_id'],
        keyword = request.form.get("keyword"),
        important = request.form.get("important"),
        sort_by = request.form.get("sort_by"),
        order = request.form.get("order")
    )
    update_dto = MemoUpdateDTO(
        memo_id = request.form.get("memo_id"),
        user_id = session['user_id'],
        content = request.form.get("content")
    )

    mm.update_memo(update_dto)

    return redirect(
        url_for(
            "memo.main",
            keyword = filter_dto.keyword,
            important = filter_dto.important_query,
            sort_by = filter_dto.sort_by,
            order = filter_dto.order
        )
    )


    

