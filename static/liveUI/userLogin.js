// Consume API here
'use strict'; // Use ES6

// Some variables defined in common_funcs.js

// Login normal user
function loginUser(endpoint) {
    // collect credentials into an object
    let data = {
        "email": loginEmailInput.value,
        "password": loginPasswordInput.value
    };

    // Send POST request to admin login page
    fetch(`${api_url}/${endpoint}`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }

    })
    .then((response)=> {
        return response.json()
    })
    .then(function(responseJSON) {
        let message = responseJSON.message;
        if(message === "Login successful.") {
            // Store user_token in localStorage
            localStorage.userToken = responseJSON.user.auth_token;
            localStorage.loggedInAs = responseJSON.user.username;
            // Redirect to orders page
            window.location.replace("../users/place_order.html");

        }
        else if(message === "Admin logged in") {
            // Store admin_token in localStorage
            localStorage.adminToken = responseJSON.admin.token;
            localStorage.loggedInSince = responseJSON.admin.logged_in_at;
            // Redirect to orders page
            window.location.replace("../orders.html");
        }
        else {
            // Add message to warning paragrapgh
            warningWrongLogins.innerHTML = message;
            // Append message to login form
            loginBtn.parentNode.insertBefore(warningWrongLogins, loginBtn);
            highlightWrongInputOnForm(message);

        }
    })
    .catch(function(err) {
        console.log(err);
    });
}


// Click listener for login btn
// Defined in common_funcs.js
addListenersToLoginBtns();
