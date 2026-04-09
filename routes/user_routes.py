from flask import request, redirect, session, Blueprint,render_template
from  models.user_model import UserModel
um = UserModel()
user_bp = Blueprint("user", __name__)
@user_bp.route("/sign_up", methods=["POST"])
def sign_up():
    login_id = request.form.get("login_id")
    if um.check_id_duplication(login_id):
        return render_template("sign_up.html",server_msg = "이미 존재하는 아이디입니다.")
    passwd = request.form.get("passwd")
    user_name = request.form.get("user_name")
    um.sign_up(login_id, passwd, user_name)
    return redirect("/sign_in")
@user_bp.route("/sign_in", methods=["POST"])
def sign_in():
    login_id = request.form.get("login_id")
    passwd = request.form.get("passwd")
    user_id = um.sign_in(login_id, passwd)
    if user_id is None:
        return render_template("sign_in.html" ,server_msg = "아이디 또는 비밀번호가 틀렸습니다.")
    session["user_id"] = user_id
    return redirect("/")
@user_bp.route("/sign_in")
def sign_in_form():
    return render_template("sign_in.html")
@user_bp.route("/sign_up")
def sign_up_form():
    return render_template("sign_up.html")

    