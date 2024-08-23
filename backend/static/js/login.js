function setCookie(cname, cvalue, exhours=null) {
    const d = new Date();
    if (exhours === null) {
        document.cookie = cname + "=" + cvalue;
    }
    else {
        d.setTime(d.getTime() + (exhours*60*60*1000));
        let expires = "expires="+ d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires; // + ";path=/";
    }
}

async function login() {
    const username = document.getElementById('username-input').value;
    console.log(`Username is ${username}`);
    const password = document.getElementById('password-input').value;
    console.log(`Password is ${password}`);

    const base_url = window.location.origin;
    const path = "/api/token";
    const url = `${base_url}${path}`;
    console.log(url);

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

    if (resp.status != 200) {
        alert("Invalid username or password.");
        return;
    }
    
    const resp_json = await resp.json();
    console.log(resp_json);
    const token = await resp_json["access_token"];
    
    
    setCookie("access_token", token, 4)
    // document.cookie = `token=${}` //; expires=Thu, 18 Dec 2013 12:00:00 UTC;`
    
    window.location.replace("/home")

}