var globalState = null;
var messageInterval = null;
var lastMessages = [];

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
    if (add_contact_input.value.trim() === "") { 
        alert("لطفا آی دی را وارد کنید."); 
    } else {
        add_contact_form.submit();
    }
}

function addContact() {
    if (globalState === null || globalState !== "add-contact") {
        try { sidebar.removeChild(message_div); } catch {}

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

async function send_message_api(toid, message) {
    const url = `/send-message?message=${encodeURIComponent(message)}&toid=${encodeURIComponent(toid.toLowerCase())}`;

    try {
        const response = await fetch(url, { method: 'GET' });
        const data = await response.json();

        if (!response.ok) {
            return { success: false, error: data.error || 'Server error' };
        }

        return data;
    } catch (error) {
        console.error('Network error:', error);
        return { success: false, error: 'Network error' };
    }
}

async function sendMessage(target_name, username) {
    const messageArea = document.querySelector("textarea.message-input");
    const message = messageArea.value.trim();

    if (!message) {
        alert("نمیتوانید پیام خالی بفرستید.");
        return;
    }

    const result = await send_message_api(target_name, message);

    if (result.success) {
        messageArea.value = "";
    } else {
        alert(result.error || "خطا در ارسال پیام.");
    }
}

function openUserContactBox(username, target_name) {
    try { sidebar.removeChild(add_contact_div); } catch {}

    globalState = "contact-box";

    message_div.className = "message-box";

    message_title.id = "message-title";
    message_title.innerHTML = `<p>از <u>${username}</u> به <u>${target_name}</u></p>`;
    message_div.appendChild(message_title);

    let messages_container = document.createElement("div");
    messages_container.className = "messages-container";
    message_div.appendChild(messages_container);

    message_area.className = "message-input";
    message_area.placeholder = "پیام ...";

    send_message_button.className = "send-message-btn";
    send_message_button.innerText = "↑";
    send_message_button.onclick = () => sendMessage(target_name, username);

    message_bottom.className = "audience-bottom";
    message_bottom.appendChild(message_area);
    message_bottom.appendChild(send_message_button);

    message_div.appendChild(message_bottom);
    sidebar.appendChild(message_div);

    if (messageInterval !== null) {
        clearInterval(messageInterval);
    }

    messageInterval = setInterval(() => {
        updateMessages(target_name.toLowerCase());
    }, 1000);
}

async function get_message_api(toid) {
    const url = `/get-messages?toid=${encodeURIComponent(toid.toLowerCase())}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (!response.ok) {
            return { success: false, error: data.error || "Server error" };
        }

        return data;
    } catch (error) {
        console.error("Network error:", error);
        return { success: false, error: "Network error" };
    }
}

async function updateMessages(toid) {
    const result = await get_message_api(toid);

    if (!result.success) return;

    const messages = result.data;

    if (JSON.stringify(messages) === JSON.stringify(lastMessages)) {
        return;
    }

    lastMessages = messages;

    const container = document.querySelector(".messages-container");
    if (!container) return;

    container.innerHTML = "";

    messages.forEach(msg => {
        const messageBox = document.createElement("div");
        messageBox.className = "message-div";
        messageBox.innerHTML = `
            <h2>${msg.sender}</h2>
            <pre>${msg.message}</pre>
        `;
        container.appendChild(messageBox);
    });
}
