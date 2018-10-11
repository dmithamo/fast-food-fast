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
    // Retrieve login credentials
    let email = loginEmailInput.value;
    let password = loginPasswordInput.value;
    // collect credentials into an object
    let data = {
        email: email,
        password: password
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

// Call function when login btn is clicked
loginForm.addEventListener('submit', () => {
    loginAdmin();
});
