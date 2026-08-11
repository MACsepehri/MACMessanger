function login() {
    let username = document.getElementsByName("username")[0].value;
    let password = document.getElementsByName("password")[0].value;
    let confirm_password = document.getElementsByName("confirm-password")[0].value;
    let login_form = document.getElementById("login-form");
    if (username.trim() === "" || password.trim() === "" || confirm_password.trim() === "") { alert("Please fill all entries") }
    else {
        if (password !== confirm_password) { alert("Passwords are not same."); }
        else { login_form.submit() }
    }
}