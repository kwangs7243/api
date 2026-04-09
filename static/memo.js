const form = document.querySelector("#filter_form")
const important = document.querySelector("#important")
const sort_by = document.querySelector("#sort_by")
const order = document.querySelector("#order")
important.addEventListener('change',() => {form.submit();});
sort_by.addEventListener('change',() => {form.submit();});
order.addEventListener('change',() => {form.submit();});