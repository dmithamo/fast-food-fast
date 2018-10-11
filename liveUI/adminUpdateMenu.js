// Consume API here
'use strict'; // Use ES6


// loginResp
let adminToken = localStorage.adminToken;
let loggedInSince = localStorage.loggedInSince;

// Reusable variable
let message = '';

// Select add-new-btn, editing-modal
let addNewBtn = document.querySelector("#add-new-btn");
let editingModal = document.querySelector("#editing-modal");

// select logout button
let logoutBtn = document.querySelector("#logout-link");

// Remove admin token on logout 
logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("adminToken");
});

const showMessageIfError = (message) => {
    // Create and style a special paragraph to report that menu is empty
    let specialPara = document.createElement("p");
    specialPara.classList.add("msg-paragraph");
    specialPara.innerHTML = message;

    // Append to page
    menuUL.parentNode.insertBefore(specialPara, menuUL);
};


function toggleEditingMode() {
    const editingForm = document.querySelector('#editing-modal');
    const section = document.querySelector('section');
    const footer = document.querySelector('footer');

    const elements = [editingForm, section, footer];

    for (let elem of elements) {
        elem.classList.toggle('hidden-mode');
    }
}


function addToMenu() {
    let data = {
        "food_item_name": "Juice na Njugu",
        "food_item_price": 400
    };

    fetch(`${api_url}/menu`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${adminToken}`
        }
    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        message = responseJSON.message;
        if(message !== "Food item added succesfully.") {
            // Show message
            showMessageIfError(message);
        }
        else {
            // Reload menu page
            window.location.replace("adm_menu.html");
        }

        })
    .catch(function(error) {
        console.log(error);
    });
}

// On document ready
document.addEventListener('DOMContentLoaded', () => {
    if(adminToken){
        addToMenu();
    }
    else {
        showMessageIfError(`Please <a class="adm-login-link" href="login.html">login as admin here.</a>`);
    }
});

// On clicking add-new-btn
addNewBtn.addEventListener('click', () => {
    if(adminToken){
        toggleEditingMode();
    }
    else {
        showMessageIfError(`Please <a class="adm-login-link" href="login.html">login as admin here.</a>`);
    }
});
