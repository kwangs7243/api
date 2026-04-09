const filterForm = document.querySelector("#filter_form");
const important = document.querySelector("#important");
const sortBy = document.querySelector("#sort_by");
const order = document.querySelector("#order");

const addForm = document.querySelector("#add_form");
const addContent = document.querySelector("#add_content");
const addFormMsg = document.querySelector("#add_form_msg");

const updateForms = document.querySelectorAll(".update_form");
const deleteForms = document.querySelectorAll(".delete_form");


if (important) {
    important.addEventListener("change", function () {
        filterForm.submit();
    });
}

if (sortBy) {
    sortBy.addEventListener("change", function () {
        filterForm.submit();
    });
}

if (order) {
    order.addEventListener("change", function () {
        filterForm.submit();
    });
}


if (addForm) {
    addForm.addEventListener("submit", function (e) {
        const value = addContent.value.trim();

        if (value === "") {
            e.preventDefault();
            addFormMsg.innerText = "메모 내용은 공백만 입력할 수 없습니다.";
            addContent.focus();
            return;
        }

        if (value.length > 100) {
            e.preventDefault();
            addFormMsg.innerText = "메모는 100자 이하로 입력하세요.";
            addContent.focus();
            return;
        }

        addFormMsg.innerText = "";
    });
}


updateForms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
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
    });
});

// 메모 삭제 확인
deleteForms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
        const ok = confirm("이 메모를 삭제하시겠습니까?");
        if (!ok) {
            e.preventDefault();
        }
    });
});