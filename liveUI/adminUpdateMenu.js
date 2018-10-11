// Consume API here
'use strict'; // Use ES6


// loginResp
let adminToken = localStorage.adminToken;
let loggedInSince = localStorage.loggedInSince;

// Reusable variables
let message = '';

// Div to display errors
let errorDiv = document.createElement("div");
errorDiv.classList.add("msg-paragraph");

// p tag with error
let specialPara = document.createElement("p");
// append to errorDiv
errorDiv.appendChild(specialPara);

// button to close error div
let closeBtn = document.createElement("button");
closeBtn.classList.add("close-btn");
closeBtn.innerHTML = "Close";
closeBtn.id = "close-btn";
// appedn to errorDiv
errorDiv.appendChild(closeBtn);


// Append to page
menuUL.parentNode.parentNode.insertBefore(errorDiv, menuUL.parentNode);
// Hide since it currently is empty
errorDiv.classList.add("hidden-mode");

// Select add-new-btn, editing-modal, save-btn, cancel-btn
let addNewBtn = document.querySelector("#add-new-btn");
let editingModal = document.querySelector("#editing-modal");
let saveNewBtn = document.querySelector("#save-new-btn");
let cancelBtn = document.querySelector("#cancel-btn");
closeBtn = document.querySelector("#close-btn");

// select logout button
let logoutBtn = document.querySelector("#logout-link");

// Select footer, section, editing-modal to hide and show as necessary
const editingForm = document.querySelector('#editing-modal');
const section = document.querySelector('section');
const footer = document.querySelector('footer');

// Collect new food item attributes
let foodItemName = document.querySelector("#new-item-name");
let foodItemPrice = document.querySelector("#new-item-price");

// Remove admin token on logout 
logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("adminToken");
});

const showMessageIfError = (message) => {
    // Show error message
    specialPara.innerHTML = message;
    // Hide everything else
    for(let tag of [section, footer]) {
        tag.classList.add("hidden-mode");
    }
    // Reveal errorDiv
    errorDiv.classList.remove("hidden-mode");
};

function addToMenu() {
    let data = {
        "food_item_name": foodItemName.value,
        "food_item_price": +foodItemPrice.value
    };
    // POST menu item
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
        if(message === "Food item added succesfully.") {
            // Reload menu page
            window.location.replace("adm_menu.html");
        }
        else {
            // Show message
            showMessageIfError(message);
        }

        })
    .catch(function(error) {
        console.log(error);
    });
}

// On clicking add-new-btn or save btn
for(let btn of [addNewBtn, saveNewBtn, cancelBtn, closeBtn]){
   btn.addEventListener('click', () => {
    if(adminToken){
        // Hide or reveal on function call
        for (let tag of [editingForm, section, footer]) {
            tag.classList.toggle('hidden-mode');
        }
        if(btn.value === "Save"){
            // Make POST request to server
            addToMenu();
        }
        else if(btn.innerHTML === "Close" || btn.value === "Cancel") {
            window.location.replace("adm_menu.html");
        }
    }
    else {
        showMessageIfError(`Please <a class="adm-login-link" href="login.html">login as admin here.</a>`);
    }
   });
}

// On page load
document.addEventListener('DOMContentLoaded', () => {
    if(!adminToken) {
        errorDiv.lastChild.remove();
        showMessageIfError(`Please <a class="adm-login-link" href="login.html">login as admin here.</a>`);
    }
});

