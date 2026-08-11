function AddContact() {
    let add_contact_form = document.getElementById("add-contact-form");
    let publicID = document.getElementById("publicID").value;
    if (publicID.trim() === "") { alert("Please enter a public id to continue."); }
    else { add_contact_form.submit(); }
}

function showAndHideContactBox() {
    let contact_box = document.querySelector("div.add-contact");
    if (contact_box.style.display === "block") { contact_box.style.display = "none"; }
    else { contact_box.style.display = "block"; }
}