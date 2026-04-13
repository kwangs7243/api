from flask import Flask ,session,redirect,render_template
from routes.user_routes import user_bp
from routes.memo_routes import memo_bp
from routes.todo_routes import todo_bp
from routes.accountbook_routes import accountbook_bp
from models.user_model import UserModel
um = UserModel()
app = Flask(__name__)
app.register_blueprint(memo_bp, url_prefix="/memo")
app.register_blueprint(todo_bp, url_prefix="/todo")
app.register_blueprint(accountbook_bp, url_prefix="/accountbook")
app.register_blueprint(user_bp)
app.secret_key = "your_secret_key"
@app.route("/")
def main():
    if not "user_id" in session:
        return redirect("/sign_in")
    user_id = session["user_id"]
    name = um.get_user_name(user_id=user_id)
    return render_template("index.html" , name = name)
@app.route("/sign_out")
def sign_out():
    session.clear()
    return redirect("/sign_in")
if __name__ == "__main__":
    app.run(debug=True)
        
