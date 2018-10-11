// Consume API here
'use strict'; // Use ES6

const api_url = "https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2";

// Login Btn and forms
const loginBtn = document.querySelector("#login-btn");
const loginForm = document.querySelector("#login-form");
const loginEmailInput = document.querySelector("#login-email-input");
const loginPasswordInput = document.querySelector("#login-password-input");

// Create and style a p tag for error message on login
let warningWrongLogins = document.createElement("p");
warningWrongLogins.classList.add("p-logins-warning");

// Helper function
const appendToparent = (element, parent) => {
    parent.appendChild(element);
};

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

// If email and password fields have values
// Call loginAdmin when login btn is clicked 
loginBtn.addEventListener('click', (event) => {
    if(loginEmailInput.value && loginPasswordInput.value) {
        event.preventDefault();
        loginAdmin();
    }
});

// Also call loginAdmin when Enter key is pressed
document.addEventListener("keypress", (event) => {
    if(loginEmailInput.value && loginPasswordInput.value) {
        if(event.keyCode === 13) {
            event.preventDefault();
            loginAdmin();
        }
    }
});