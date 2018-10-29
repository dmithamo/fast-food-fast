// Consume API here
'use strict'; // Use ES6

// Register Btn and forms
let registerBtn = document.querySelector("#register-btn");
let registerUsernameInput = document.querySelector("#register-username-input");
let registerEmailInput = document.querySelector("#register-email-input");
let registerPasswordInput = document.querySelector("#register-password-input");
let confirmPasswordInput = document.querySelector("#confirm-password-input");


function registerUser() {
    // collect credentials into an object
    let data = {
        "username": registerUsernameInput.value,
        "email": registerEmailInput.value,
        "password": registerPasswordInput.value
    };

    // Send POST request to admin login page
    fetch(`${api_url}/auth/signup`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }

    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        let message = responseJSON.message;
        if(message === "Registration successful") {
            // Add message to warning paragrapgh
            warningWrongLogins.innerHTML = `${message}. Login to continue. Redirecting ...`;
            // Style green for success
            warningWrongLogins.classList.add("msg-success");
            warningWrongLogins.classList.add("resp-message");
            // Append message to login form
            registerBtn.parentNode.insertBefore(warningWrongLogins, registerBtn);

            // Redirect to login page
            setTimeout(() => {
                window.location.replace("login.html");
            }, 5000);

        }
        else {
            // Add message to warning paragrapgh
            warningWrongLogins.classList.add("resp-message");
            warningWrongLogins.innerHTML = message;
            // Append message to registration form
            registerBtn.parentNode.insertBefore(warningWrongLogins, registerBtn);
            // Highlight the input with wrong value, if any
            highlightWrongInputOnForm(message);

        }
    })
    .catch(function(err) {
        console.log(err);
    });
}


// If email and password fields have values
// Call registerUser when register btn is clicked 
registerBtn.addEventListener('click', (event) => {
    if(registerUsernameInput.value && registerEmailInput.value &&  registerPasswordInput.value) {
        if(registerPasswordInput.value === confirmPasswordInput.value) {
            event.preventDefault();
            registerUser();
            for(let input of [registerPasswordInput, confirmPasswordInput]) {
                input.classList.remove("wrong-input");
            }
        }
        else {
            event.preventDefault();
            warningWrongLogins.innerHTML = "Passwords do not match!";
            warningWrongLogins.classList.add('resp-message')
            confirmPasswordInput.parentNode.insertBefore(warningWrongLogins, confirmPasswordInput);
            for(let input of [registerPasswordInput, confirmPasswordInput]) {
                input.classList.add("wrong-input");
            }
        }
    }
});

// Also call registerUser when Enter key is pressed
registerBtn.addEventListener('keypress', (event) => {
    if(event.keyCode === 13) {
        if(registerUsernameInput.value && registerEmailInput.value &&  registerPasswordInput.value) {
            if(registerPasswordInput.value === confirmPasswordInput.value) {
                event.preventDefault();
                registerUser();
            }
            else {
                event.preventDefault();
                warningWrongLogins.innerHTML = "Passwords do not match!";
                warningWrongLogins.classList.add('resp-message')
                confirmPasswordInput.parentNode.insertBefore(warningWrongLogins, confirmPasswordInput);
            }
        }
    }
});
