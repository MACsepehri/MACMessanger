var globalState = null;

let add_contact_div = document.createElement("div");
let add_contact_form = document.createElement("form");
let add_contact_input = document.createElement("input");
let add_contact_button = document.createElement("button");

let sidebar = document.querySelector("div.left-content");

function checkAddingContact() {
    if (add_contact_input.value.trim() === "") { alert("لطفا آی دی را وارد کنید."); }
    else {
        add_contact_form.submit();
    }
}

function addContact() {
    if (globalState === null || globalState !== "add-contact") {
        add_contact_div.className = "add-contact-box";
        add_contact_form.action = "/add-contact";
        add_contact_form.method = "post";
        add_contact_input.name = "id";
        add_contact_input.type = "text";
        add_contact_input.placeholder = "آی دی";
        add_contact_form.id = "id-input";
        add_contact_button.className = "add-contact-btn";
        add_contact_button.innerText = "اضافه کردن";
        add_contact_button.onclick = checkAddingContact;

        add_contact_form.appendChild(add_contact_input);
        add_contact_div.appendChild(add_contact_form);
        add_contact_div.appendChild(add_contact_button);
        sidebar.appendChild(add_contact_div);
        globalState = "add-contact";
    }
}