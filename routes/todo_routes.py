from flask import Blueprint, session, redirect, render_template, request
from models.todo_model import TodoModel
from models.user_model import UserModel
tm = TodoModel()
um = UserModel()
todo_bp = Blueprint("todo",__name__)
@todo_bp.route("/")
def main():
    if "user_id" not in session:
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
    if  sort_by not in ["created_at","content","completed"]:
        sort_by = "created_at"
    order = request.args.get("order" , "desc")
    order = order.lower()
    if  order not in ["asc" , "desc"]:
        order = "desc"
    name = um.get_user_name(user_id)
    todos = tm.get_user_todos(
                user_id, keyword = keyword, completed = completed,
                sort_by = sort_by, order = order)
    return render_template(
            "todo.html",
            todos = todos, keyword = keyword, completed = completed,
            sort_by = sort_by, order = order, name = name)
@todo_bp.route("/add", methods = ["POST"])
def add():
    if "user_id" not in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    keyword = request.form.get("keyword","")
    content = request.form.get("content")
    completed = request.form.get("completed")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")
    tm.add_todo(user_id, content)
    return redirect(f"/todo?&keyword={keyword}&completed={completed}&sort_by={sort_by}&order={order}")
@todo_bp.route("/delete", methods=["POST"])
def delete():
    if "user_id" not in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    todo_id = request.form.get("todo_id")
    keyword = request.form.get("keyword","")
    completed = request.form.get("completed")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")
    tm.delete_todo(todo_id, user_id)
    return redirect(f"/todo?&keyword={keyword}&completed={completed}&sort_by={sort_by}&order={order}")
@todo_bp.route("/completed", methods = ["POST"])
def completed():
    if "user_id" not in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    todo_id = request.form.get("todo_id")
    keyword = request.form.get("keyword","")
    completed = request.form.get("completed")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")
    tm.set_completed(todo_id, user_id)
    return redirect(f"/todo?&keyword={keyword}&completed={completed}&sort_by={sort_by}&order={order}")
@todo_bp.route("/update", methods = ["POST"])
def update():
    if "user_id" not in session:
        return redirect("/sign_in")
    user_id = session['user_id']
    todo_id = request.form.get("todo_id")
    content = request.form.get("update")
    keyword = request.form.get("keyword","")
    completed = request.form.get("completed")
    sort_by = request.form.get("sort_by")
    order = request.form.get("order")
    tm.update_todo(todo_id, user_id, content)
    return redirect(f"/todo?&keyword={keyword}&completed={completed}&sort_by={sort_by}&order={order}")

