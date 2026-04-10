const sign_up_form = document.querySelector("#sign_up");
const login_id = document.querySelector("[name='login_id']");
const user_name = document.querySelector("#user_name");
const passwd = document.querySelector("#passwd");
const passwd_check = document.querySelector("#passwd_check");

if (login_id) {
    login_id.addEventListener(
        "input",function(){
            if (login_id.value.trim().length < 6){
                sign_up_form.querySelector("#msg").textContent = "아이디는 5글자이상 입력하세요";
                sign_up_form.querySelector("#msg").style.color = 'red';
            }else{
                sign_up_form.querySelector("#msg").textContent = "";
            }

        })
    }

if (sign_up_form) {
    sign_up_form.addEventListener(
        "submit",function(e){
            if (login_id.value.trim() === "") {
                sign_up_form.querySelector("#msg").textContent = "아이디를 입력하세요";
                sign_up_form.querySelector("#msg").style.color = 'red';
                e.preventDefault();
                login_id.focus();
                return;
            }
            if (user_name.value.trim() === "") {
                sign_up_form.querySelector("#msg").textContent = "이름을 입력하세요";
                sign_up_form.querySelector("#msg").style.color = 'red';
                e.preventDefault();
                user_name.focus();
                return;
            }
            if (passwd.value.trim() === "") {
                sign_up_form.querySelector("#msg").textContent = "비밀번호를 입력하세요";
                sign_up_form.querySelector("#msg").style.color = 'red';
                e.preventDefault();
                passwd.focus();
                return;
            }
            if (passwd.value.trim() != passwd_check.value.trim()) {
                sign_up_form.querySelector("#msg").textContent = "비밀번호확인이 다릅니다";
                sign_up_form.querySelector("#msg").style.color = 'red';
                e.preventDefault();
                passwd.focus();
                return;
            }
        })
    }

