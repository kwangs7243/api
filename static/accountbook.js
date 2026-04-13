const filter_form = document.querySelector("#filter_form")
const category = document.querySelector("#category")
const sort_by = document.querySelector("#sort_by")
const order = document.querySelector("#order")
const keyword = document.querySelector("#keyword")

if (category) {
    category.addEventListener(
        "change", function() {
            filter_form.submit();
        }
    )
}

if (sort_by) {
    sort_by.addEventListener(
        "change", function() {
            filter_form.submit();
        }
    )
}

if (order) {
    order.addEventListener(
        "change", function() {
            filter_form.submit();
        }
    )
}

const add_form = document.querySelector("#add_form")

if (add_form) {
    add_form.addEventListener(
        "submit", function(e) {
            let msg = document.querySelector("#add_form_msg")
            let amount = add_form.querySelector("#add_amount")
            if (amount.value.trim() === "") {
                e.preventDefault();
                msg.textContent = " 금액은 공백으로 입력 할 수 없습니다.";
                msg.style.color = "red";
                amount.focus();
                return;
            }
            let content = add_form.querySelector("#add_content")
            if (content.value.trim() === "") {
                e.preventDefault();
                msg.textContent = " 내용은 공백으로 입력 할 수 없습니다.";
                msg.style.color = "red";
                content.focus()
                return;
            }
            msg.textContent = ""
        }
    )
}

const update_forms = document.querySelectorAll(".update_form")

if (update_forms) {
    update_forms.forEach(function(form) {
        form.addEventListener(
            "submit", function(e) {
                let amount = form.querySelector("[name=update_amount]")
                if (amount.value.trim() === "") {
                    e.preventDefault();
                    alert("수정 금액은 공백으로 입력 할 수 없습니다.");
                    amount.focus();
                    return;
                }
                let content = form.querySelector("[name=update_content]")
                if (content.value.trim() === "") {
                    e.preventDefault();
                    alert("수정 내용은 공백으로 입력 할 수 없습니다.");
                    content.focus();
                    return;
                }
            }
        )
    })
}

const delete_forms = document.querySelectorAll(".delete_form")

if (delete_forms) {
    delete_forms.forEach(function(form) {
        form.addEventListener(
            "submit", function(e) {
                let ok = confirm("이 메모를 삭제하시겠습니까?");
                if (!ok) {
                    e.preventDefault();
                }
            }
        )
    })
}
