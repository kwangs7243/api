const filterform = document.querySelector("#filter_form");
const important = document.querySelector("#important");
const sortBy = document.querySelector("#sort_by");
const order = document.querySelector("#order");

const addform = document.querySelector("#add_form");
const addcontent = document.querySelector("#add_content");
const addformmsg = document.querySelector("#add_form_msg");

const updateforms = document.querySelectorAll(".update_form");
const deleteforms = document.querySelectorAll(".delete_form");


if (important) {
    important.addEventListener(
        "change", function () {
        filterform.submit();
    })
}

if (sortBy) {
    sortBy.addEventListener(
        "change", function () {
        filterform.submit();
    })
}

if (order) {
    order.addEventListener(
        "change", function () {
        filterform.submit();
    })
}


if (addform) {
    addform.addEventListener(
        "submit", function (e) {
        const value = addcontent.value.trim();

        if (value === "") {
            e.preventDefault();
            addformmsg.innerText = "메모 내용은 공백만 입력할 수 없습니다.";
            addcontent.focus();
            return;
        }

        if (value.length > 100) {
            e.preventDefault();
            addformmsg.innerText = "메모는 100자 이하로 입력하세요.";
            addcontent.focus();
            return;
        }

        addformmsg.innerText = "";
    })
}


updateforms.forEach(function (form) {
    form.addEventListener(
        "submit", function (e) {
        const updateInput = form.querySelector("[name='update']");
        const value = updateInput.value.trim();

        if (value === "") {
            e.preventDefault();
            alert("수정 내용은 비어 있을 수 없습니다.");
            updateInput.focus();
            return;
        }

        if (value.length > 100) {
            e.preventDefault();
            alert("수정 내용은 100자 이하로 입력하세요.");
            updateInput.focus();
            return;
        }
    })
})

// 메모 삭제 확인
deleteforms.forEach(function (form) {
    form.addEventListener(
        "submit", function (e) {
        const ok = confirm("이 메모를 삭제하시겠습니까?");
        if (!ok) {
            e.preventDefault();
        }
    })
})