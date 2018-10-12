// Consume API here
'use strict'; // Use ES6

const api_url = "https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2";

// Create and style a p tag for error message on login
let warningWrongLogins = document.createElement("p");
warningWrongLogins.classList.add("p-logins-warning");

// Login Btn and forms
let loginBtn = document.querySelector("#login-btn");
let loginEmailInput = document.querySelector("#login-email-input");
let loginPasswordInput = document.querySelector("#login-password-input");

// Helper function
const appendToparent = (element, parent) => {
    parent.appendChild(element);
};


function loginUser() {
    // collect credentials into an object
    let data = {
        "email": loginEmailInput.value,
        "password": loginPasswordInput.value
    };

    // Send POST request to admin login page
    fetch(`${api_url}/auth/login`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }

    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        let message = responseJSON.message;
        if(message === "Login successful.") {
            // Store user_token in localStorage
            localStorage.userToken = responseJSON.user.auth_token;
            localStorage.loggedInAs = responseJSON.user.username;
            // Redirect to orders page
            window.location.replace("../users/orders.html");

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


// If email and password fields have values
// Call loginUser when login btn is clicked 
loginBtn.addEventListener('click', (event) => {
    if(loginEmailInput.value && loginPasswordInput.value) {
        event.preventDefault();
        loginUser();
    }
});

// Also call loginUser when Enter key is pressed
document.addEventListener("keypress", (event) => {
    if(event.keyCode === 13) {
        if(loginEmailInput.value && loginPasswordInput.value) {
            event.preventDefault();
            loginUser();
        }
    }
});
