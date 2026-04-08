from flask import request, redirect, session, Blueprint
from  models.user_model import UserModel
um = UserModel()
user_bp = Blueprint("user", __name__)
@user_bp.route("/sign_up", methods=["POST"])
def sign_up():
    login_id = request.form.get("login_id")
    if um.check_id_duplication(login_id):
        return "이미 존재하는 아이디입니다."
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
        return "아이디 또는 비밀번호가 틀렸습니다."
    session["user_id"] = user_id
    return redirect("/")
@user_bp.route("/sign_in")
def sign_in_form():
    return '''
    <form method="post" action="/sign_in">
        <input type="text" name="login_id" placeholder="아이디" required>
        <input type="password" name="passwd" placeholder="비밀번호" required>
        <button type="submit">로그인</button>
    </form>
    <a href="/sign_up">회원가입</a>
    '''
@user_bp.route("/sign_up")
def sign_up_form():
    return '''
    <form method="post" action="/sign_up">
        <input type="text" name="login_id" placeholder="아이디" required>
        <input type="password" name="passwd" placeholder="비밀번호" required>
        <input type="text" name="user_name" placeholder="이름" required>
        <button type="submit">회원가입</button>
    </form>
    <a href="/sign_in">로그인</a>
    '''

    