console.log('Hello world');

function create_new_user() {
    let username = document.getElementById('username-input').value
    // console.log(`Username is ${username}`);
    let password = document.getElementById('password-input').value
    // console.log(`Password is ${password}`);
    let password_confirm = document.getElementById('confirm-password-input').value
    // console.log(`Password confirm is ${password_confirm}`);
    
    if (password !== password_confirm) {
        alert("Passwords do NOT match!")
        return;
    }
    
    console.log("Check passed!");
    // TODO: continue here
    
}
