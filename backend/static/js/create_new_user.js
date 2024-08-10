console.log('Hello world');

async function create_new_user() {
    const username = document.getElementById('username-input').value;
    // console.log(`Username is ${username}`);
    const password = document.getElementById('password-input').value;
    // console.log(`Password is ${password}`);
    const password_confirm = document.getElementById('confirm-password-input').value;
    // console.log(`Password confirm is ${password_confirm}`);
    
    if (password !== password_confirm) {
        alert("Passwords do NOT match!");
        return;
    }
    
    console.log("Check passed!");
    const base_url = window.location.origin;
    const path = "/users/add";
    const url = `${base_url}${path}`;
    console.log(url);
    
    // TODO: test

    const resp = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "username": username,
                "password": password
            }),
        }
    );
    console.log(resp);
    console.log(resp.json());
    
    if (resp.status == 200) {
        window.location.replace("/")
    }
}
