const sign_up_form = document.querySelector("#sign_up");
const login_id = document.querySelector("[name='login_id']");

if (login_id) {
    login_id.addEventListener(
        "input",function(e){
            if (login_id.value.trim().length < 6){
                sign_up_form.querySelector("#msg").textContent = "아이디는 5글자이상 입력하세요";
                sign_up_form.querySelector("#msg").style.color = 'green';
            }else{
                sign_up_form.querySelector("#msg").textContent = "";
            };

        });
    };

