const sign_in = document.querySelector("#sign_in");
const login_id = document.querySelector("[name=login_id]");
const password = document.querySelector("[name=passwd]");

if (login_id) {
    login_id.addEventListener(
        "input",function(){
            if (0 < login_id.value.trim().length && login_id.value.trim().length < 5) {
                sign_in.querySelector("#msg").textContent = "아이디는 5글자이상 입력하세요";
                sign_in.querySelector("#msg").style.color = "red";
            }else{
                sign_in.querySelector("#msg").textContent = "";
            }
        }
    )
}

if (sign_in) {
    sign_in.addEventListener(
        "submit",function(e){
            if (login_id.value.trim() === ""){
                sign_in.querySelector("#msg").textContent = "아이디를 입력하세요";
                e.preventDefault();
                login_id.focus();
                return;
            }
            if (password.value.trim() === ""){
                sign_in.querySelector("#msg").textContent = "비밀번호를 입력하세요";
                e.preventDefault();
                password.focus();
                return;
            }
        }
    )
}