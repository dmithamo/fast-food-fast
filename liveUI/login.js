// Consume API here
'use strict'; // Use ES6

const api_url = "https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2";

// Login
const loginBtn = document.querySelector("#login-btn");
const loginEmailInput = document.querySelector("#login-email-input");
const loginPasswordInput = document.querySelector("#login-password-input");


// Helper function
const appendToparent = (element, parent) => {
    parent.appendChild(element);
};

function loginAdmin() {
    // Retrieve login credentials
    let email = loginEmailInput.innerHTML;
    let password = loginPasswordInput.innerHTML;
    console.log(email, password);


    // fetch(`${api_url}/login`, {

    // })
    // .then((response) => response.json())
    // .then(function(responseJSON) {
    //     console.log(responseJSON);

    // })
    // .catch(function(err) {
    //     console.log(err);
    // })
}

// Call function when login btn is clicked
loginBtn.addEventListener('click', () => {
    loginAdmin();
});



