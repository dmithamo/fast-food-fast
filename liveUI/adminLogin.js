// Consume API here
'use strict'; // Use ES6

function loginAdmin() {
    // collect credentials into an object
    let data = {
        "email": loginEmailInput.value,
        "password": loginPasswordInput.value
    };

    // Send POST request to admin login page
    fetch(`${api_url}/login`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }

    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        let message = responseJSON.message;
        if(message === "Admin logged in") {
            // Store admin_token in localStorage
            localStorage.adminToken = responseJSON.admin.token;
            localStorage.loggedInSince = responseJSON.admin.logged_in_at;
            // Redirect to orders page
            window.location.replace("orders.html");

        }
        else {
            // Add message to warning paragrapgh
            warningWrongLogins.innerHTML = message;
            // Append message to login form
            loginBtn.parentNode.insertBefore(warningWrongLogins, loginBtn);
        }
    })
    .catch(function(err) {
        console.log(err);
    });
}

// Click listener for login btn
// Defined in common_funcs.js
addListenersToLoginBtns(loginAdmin);