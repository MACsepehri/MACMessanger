var globalState = null;

let add_contact_div = document.createElement("div");
let add_contact_form = document.createElement("form");
let add_contact_input = document.createElement("input");
let add_contact_button = document.createElement("button");

let message_div = document.createElement("div");
let message_title = document.createElement("p");
let message_bottom = document.createElement("div");
let message_area = document.createElement("textarea");
let send_message_button = document.createElement("button");

let sidebar = document.querySelector("div.left-content");

function checkAddingContact() {
    if (add_contact_input.value.trim() === "") { alert("لطفا آی دی را وارد کنید."); }
    else {
        add_contact_form.submit();
    }
}

function addContact() {
    if (globalState === null || globalState !== "add-contact") {
        try { sidebar.removeChild(message_div); }
        catch {}
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

function openUserContactBox(username, target_name) {
    try { sidebar.removeChild(add_contact_div); }
    catch {}

    globalState = "contact-box";

    message_div.className = "message-box";

    message_title.id = "message-title";
    message_title.innerHTML = `<p>از <u>${username}</u> به <u>${target_name}</u></p>`;

    message_area.className = "message-input";
    message_area.placeholder = "پیام ...";

    send_message_button.className = "send-message-btn";
    send_message_button.innerText = "↑";

    message_bottom.className = "audience-bottom";

    message_bottom.appendChild(message_area);
    message_bottom.appendChild(send_message_button);
    message_div.appendChild(message_title);
    message_div.appendChild(message_bottom);
    sidebar.appendChild(message_div);
}