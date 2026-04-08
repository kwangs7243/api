from flask import Flask ,session,redirect
from routes.user_routes import user_bp
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.register_blueprint(user_bp)
@app.route("/")
def home():
    if not "user_id" in session:
        return redirect("/sign_in")
    return f"로그인된 user_id: {session['user_id']}<br><a href='/sign_out'>로그아웃</a>" 
@app.route("/sign_out")
def sign_out():
    session.clear()
    return redirect("/sign_in")


if __name__ == "__main__":
    app.run(debug=True)
        
