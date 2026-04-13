from flask import Flask ,session,redirect,render_template
from routes.user_routes import user_bp
from routes.memo_routes import memo_bp
from routes.todo_routes import todo_bp
from routes.accountbook_routes import accountbook_bp
from models.user_model import UserModel
from models.memo_model import MemoModel
from models.todo_model import TodoModel
from models.accountbook_model import AccountBookModel
um = UserModel()
mm = MemoModel()
tm = TodoModel()
am = AccountBookModel()

app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix="/sign")
app.register_blueprint(memo_bp, url_prefix="/memo")
app.register_blueprint(todo_bp, url_prefix="/todo")
app.register_blueprint(accountbook_bp, url_prefix="/accountbook")
app.secret_key = "your_secret_key"
@app.route("/")
def main():
    if not "user_id" in session:
        return redirect("/sign/in")
    user_id = session["user_id"]
    name = um.get_user_name(user_id=user_id)

    recent_memos = mm.get_recent_memos(user_id)
    summary_memo = mm.get_summary_memo(user_id)

    summary_todo = tm.get_summary_todo(user_id)
    recent_todos = tm.get_recent_todos(user_id)

    summary_transaction = am.get_summary_transaction(user_id)

    summary_transaction["total_balance"] = f"{summary_transaction['total_balance']:,}"
    summary_transaction["income_sum"] = f"{summary_transaction['income_sum']:,}"
    summary_transaction["expense_sum"] = f"{summary_transaction['expense_sum']:,}"

    recent_transactions = am.get_recent_transactions(user_id)
    for transaction in recent_transactions:
        transaction["amount"] = f"{transaction['amount']:,}"

    return render_template(
        "index.html" , 
        name = name, recent_memos=recent_memos, summary_memo=summary_memo,
        summary_todo=summary_todo, recent_todos=recent_todos,
        summary_transaction=summary_transaction, recent_transactions=recent_transactions)

if __name__ == "__main__":
    app.run(debug=True)
        
