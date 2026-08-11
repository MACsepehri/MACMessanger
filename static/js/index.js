function AddContact() {
    let add_contact_form = document.getElementById("add-contact-form");
    let publicID = document.getElementById("publicID").value;
    if (publicID.trim() === "") { alert("Please enter a public id to continue."); }
    else { add_contact_form.submit(); }
}

function showAndHideContactBox() {
    let contact_box = document.querySelector("div.add-contact");
    let chatroom = document.querySelector("div.chat-room");
    if (contact_box.style.display === "block") {contact_box.style.display = "none"; }
    else {
        chatroom.style.display = "none";
        contact_box.style.display = "block";
    }
}

function StartChat(username, userid) {
    let to_username = document.getElementById("to-user");
    let chatroom = document.querySelector("div.chat-room");
    let contact_box = document.querySelector("div.add-contact");
    to_username.innerText = username;
    chatroom.style.display = "block";
    contact_box.style.display = "none";
}

function send_message(username) {
    let message = document.getElementById("message-area");
    let message_div = document.querySelector("div.messages");
    if (message.value.trim() === "") { alert("Please write a valid message."); }
    else {
        let msg = `${message.value}`;
        message.value = "";

        let mesasge_box = document.createElement("div")
        let message_box_pre_tag = document.createElement("pre")
        mesasge_box.className = "user-message";
        message_box_pre_tag.className = "message";
        message_box_pre_tag.innerHTML = `<pre id="sender">You :</pre>\n${msg}`
        mesasge_box.appendChild(message_box_pre_tag);
        message_div.appendChild(mesasge_box);
    }
}