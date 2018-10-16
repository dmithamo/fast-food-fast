'use strict';

// LINK TO HEROKU API
const api_url = "https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2";

// Login Btn and forms
let loginBtn = document.querySelector("#login-btn");
let loginEmailInput = document.querySelector("#login-email-input");
let loginPasswordInput = document.querySelector("#login-password-input");


// // Reusable variables
let message = '';

// Create and style a p tag for error message on invalid params
let warningWrongValue = document.createElement("p");
warningWrongValue.classList.add("p-logins-warning");
let warningWrongVal = warningWrongValue.cloneNode();

// Select footer
const footer = document.querySelector('footer');


// loginResp
let adminToken = localStorage.adminToken;
let loggedInSince = localStorage.loggedInSince;


// Create and style a p tag for error message on login
let warningWrongLogins = document.createElement("p");
warningWrongLogins.classList.add("p-logins-warning");

// Helper function
const appendToparent = (element, parent) => {
    parent.appendChild(element);
};


// If email and password fields have values
// Call loginUser/loginAdmin when login btn is clicked 
function addListenersToLoginBtns(funcToCall) {
    loginBtn.addEventListener('click', (event) => {
        if(loginEmailInput.value && loginPasswordInput.value) {
            event.preventDefault();
            funcToCall();
        }
    });

    // Also call loginUser when Enter key is pressed
    document.addEventListener("keypress", (event) => {
        if(event.keyCode === 13) {
            if(loginEmailInput.value && loginPasswordInput.value) {
                event.preventDefault();
                funcToCall();
            }
        }
    });
}



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

// Display error msg
const showResponseMessage = (toHide, message) => {
    // Show error message
    specialPara.innerHTML = message;
    // Hide everything else
    for(let tag of [toHide, footer]) {
        tag.classList.add("hidden-mode");
    }
    // Reveal errorDiv
    errorDiv.classList.remove("hidden-mode");
};


const showMessageIfNoItems = (attachTo, message) => {
    // Create and style a special paragraph to report that menu is empty
    let emptyPara = document.createElement("p");
    emptyPara.classList.add("msg-paragraph");
    emptyPara.innerHTML = message;

    // Append to page
    attachTo.parentNode.insertBefore(emptyPara, attachTo);
};


function styleByStatus(order, orderStatus){
    if(orderStatus === "New") {
        // Style order
        order.classList.add("new-order");
    }
    else if(orderStatus === "Processing") {
        order.classList.add("processing-order");
    }
    else if(orderStatus === "Complete") {
        order.classList.add("complete-order");
    }
    else if(orderStatus === "Cancelled") {
        order.classList.add("cancelled-order");
    }
    else if(orderStatus === "Deleted") {
        order.classList.add("deleted-order");
    }
}

function correctTime(timestamp){
    // Add 03:00:00hrs to every timestamp.
    // GMT tings
    let date = timestamp.split(" ")[0];
    let time = timestamp.split(" ")[1];
    let hours = time.split(":")[0];
    let mins = time.split(":")[1];
    let secs = time.split(":")[2];

    
    // Correct time
    let correctedHrs = +hours + 3;
    
    let correctTimestamp = `${date} ${correctedHrs}:${mins}:${secs}`;
    return correctTimestamp;
}


function addFilterOptions(optionsList) {
    // Select the select tag from page
    let selectTag = document.querySelector("select");

    // Sort optionsList, to start with statuses then usernames
    optionsList = optionsList.sort();

    // Append each option to select tag...
    for(let filterOption of optionsList){
        // If filterOption is status
        let statuses = ["New", "Processing", "Complete", "Cancelled", "Deleted"];
        if(statuses.indexOf(filterOption) > -1){
            filterOption = `status: ${filterOption}`;
        }
        else {
            // filterOption is username
            filterOption = `user: ${filterOption}`;
        }

        // Append to 'select' element on page
        let option = document.createElement("option");
        option.value = filterOption;
        option.innerHTML = filterOption;
        // Append
        selectTag.appendChild(option);
    }
    addListenersOnOptions();
}

function addListenersOnOptions() {
    // Listen for change
    // Select the select tag from page
    let selectTag = document.querySelector("select");
    selectTag.addEventListener("change",() => {
        // extract value on change
        let filter = selectTag.value.split(": ")[1];
        // Call function that filters
        filterByOption(filter);
    });
}


function filterByOption(option){
    // Hide orders where Status or Username does not match filter
    let allOrders = document.querySelectorAll(".ordered-item");
    
    // if option is All orders, show all
    if(option === "All orders") {
        for(let order of allOrders){
            order.classList.remove("hidden-mode");
        }
    }
    else {
        // for other filter options...
        for(let order of allOrders){
            let orderStatus = order.querySelector(".order-status").innerHTML.split(": ")[1];
            let orderedBy = order.querySelector(".ordered-by").innerHTML;

            // See if option matches either username or status
            // Show only orders where condition is met
            if(orderStatus !== option && orderedBy !== option) {
                order.classList.add("hidden-mode");
            }
            else {
                order.classList.remove("hidden-mode");
            }
        }
    }
}
