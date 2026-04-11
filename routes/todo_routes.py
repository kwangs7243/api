from flask import Blueprint, session, redirect, render_template, request
from models.todo_model import TodoModel
from models.user_model import UserModel
tm = TodoModel()
um = UserModel()
todo_bp = Blueprint("todo",__name__)
@todo_bp.route("/")
def main():
    if not "user_id" in session:
        return redirect("/sign_in")
    user_id = session["user_id"]
    keyword = request.args.get("keyword" , "").strip()
    completed_raw = request.args.get("completed" , False)
    if completed_raw == "1":
        completed = True
    elif completed_raw == "0":
        completed = False
    else:
        completed = None
    sort_by = request.args.get("sort_by" , "created_at")
    if not sort_by in ["created_at","content","important"]:
        sort_by = "created_at"
    order = request.args.get("order" , "desc")
    order = order.lower()
    if not order in ["asc" , "desc"]:
        order = "desc"
    name = um.get_user_name(user_id)
    todos = tm.get_user_todos(user_id,keyword=keyword,completed=completed,sort_by=sort_by,order=order)
    return render_template(
            "todo.html",
            todos=todos,keyword=keyword,completed=completed,
            sort_by=sort_by,order=order,name=name)
@todo_bp.route("/add", methods=["POST"])
def add():
    if not "user_id" in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    keyword = request.form.get("keyword","")
    content = request.form.get("content")
    completed = request.form.get("completed")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")
    tm.add_todo(user_id,content)