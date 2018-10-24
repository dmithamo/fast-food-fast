'use strict';

// LINK TO HEROKU API
const api_url = "https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2";

// Login Btn and forms
let loginBtn = document.querySelector("#login-btn");
let loginEmailInput = document.querySelector("#login-email-input");
let loginPasswordInput = document.querySelector("#login-password-input");


// Section and footer
const footer = document.querySelector('footer');
const section = document.querySelector("section");

// // Reusable variables
let message;

// Create and style a p tag for error message on invalid params
let warningWrongValue = document.createElement("p");
warningWrongValue.classList.add("p-logins-warning");
let warningWrongVal = warningWrongValue.cloneNode();


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
            if(loginEmailInput.value === "admintest@admin.com"){
                // if credentials are admin credentials
                funcToCall[0]();
            }
            // funcToCall();
            else {
                funcToCall[1]();
            }
        }
    });

    // Also call loginUser when Enter key is pressed
    document.addEventListener("keypress", (event) => {
        if(event.keyCode === 13) {
            if(loginEmailInput.value && loginPasswordInput.value) {
                event.preventDefault();
                if(loginEmailInput.value === "admintest@admin.com"){
                    // if credentials are admin credentials
                    funcToCall[0]();
                }
                else {
                    funcToCall[1]();
                }
            }
        }
    });
}



// Div to display response
let responseDiv = document.createElement("div");
responseDiv.classList.add("msg-paragraph");

// p tag with error
let specialPara = document.createElement("p");

// append to responseDiv
responseDiv.appendChild(specialPara);

// button to close error div
let closeBtn = document.createElement("button");
closeBtn.classList.add("close-btn");
closeBtn.innerHTML = "Close";
closeBtn.id = "close-btn";

// appedn to responseDiv
responseDiv.appendChild(closeBtn);

// Display error msg
const showResponseMessage = (toHide, message) => {
    // Show error message
    specialPara.innerHTML = message;
    // Hide everything else
    for(let tag of [toHide, footer]) {
        tag.classList.add("hidden-mode");
    }
    // Reveal responseDiv
    responseDiv.classList.remove("hidden-mode");
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

// Login or register form
let emailInput = document.querySelector("input[type=email]");
let usernameInput = document.querySelector("input[type=text]");
let passwordInputs = document.querySelectorAll("input[type=password]");

// Add food item to menu page
let foodItemNameInput = document.querySelector("#new-item-name");
let foodItemPriceInput = document.querySelector("#new-item-price");

// On place order page
let quantityInput = document.querySelector("#q-input-number");


// Collected in a single list
let allTheseInputTags = [emailInput, usernameInput, foodItemNameInput, foodItemPriceInput];
for(let passInput of passwordInputs){
    allTheseInputTags.push(passInput);
}

function highlightWrongInputOnForm(message) {
    // Wrong username
    if(message.indexOf("username") > -1){
        usernameInput.classList.add("wrong-input");
    }

    // Wrong email
    if(message.indexOf("email") > -1){
        emailInput.classList.add("wrong-input");
    }

    // Wrong password
    if(message.indexOf("invalid password") > -1){
        for(let pInput of passwordInputs){
            pInput.classList.add("wrong-input");
        }
    }

    // Wrong food item name
    if(message.indexOf("food_item_name") > -1 || message.indexOf("Food item name") > -1){
        foodItemNameInput.classList.add("wrong-input");
    }

    // Wrong food item price
    if(message.indexOf("food_item_price") > -1 || message.indexOf("Food item price") > -1){
        foodItemPriceInput.classList.add("wrong-input");
    }

    // Wrong quantity
    if(message.indexOf("Quantity") > -1){
        quantityInput.classList.add("wrong-input");
    }

    // Listen for user corrections
    listenForCorrections();
}

// For when user is making corrections
function listenForCorrections() {
    for(let inputTag of allTheseInputTags){
        if(inputTag){
            // If the input tag exists on current page (is not null)
            inputTag.addEventListener("change", () => {
                inputTag.classList.remove("wrong-input");
            });
        }
    }
}


// Image options
const foodImgs = {
    "Generic image": "https://15logo.net/wp-content/uploads/2017/05/fast-food-800x800.jpg",
    "Pizza": "http://www.a2zlifestyle.com/wp-content/uploads/2013/08/Healthy-and-Delicious-Pizza-at-Home.jpg",
    "Burger": "http://bk-latam-prod.s3.amazonaws.com/sites/burgerking.com.pe/files/MegaTocino_300x270px_0.png",
    "Fish": "https://img.aws.livestrongcdn.com/ls-article-image-673/cme/photography.prod.demandstudios.com/b676a889-db55-49ca-b1a1-3ced12ed8f10.jpg",
    "Soup": "https://skinnyms.com/wp-content/uploads/2012/09/Slow-Cooker-Hearty-Vegetable-and-Bean-Soup-1.jpg",
    "French fries": "http://theloadedslice.net/image/cache/products/appetizers/french-fries-800x800.png",
    "Bhajia": "http://vegindianrecipe.com/wp-content/uploads/2012/03/farali-bhajiya-large.jpg",
    "Sausage rolls": "http://richiemart.com/wp-content/uploads/2016/10/sausage-roll.jpg",
    "Milk shake": "https://www.americandairy.com/core/fileparse.php/111/urlt/vanilla-milkshake-recipe.jpg",
    "Coffee": "https://www.simplygreatcoffee.co.uk/shop/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/4/o/4oz_paper_cup_7.jpg",
};

function addImageOptions() {
    // Add image options dynamically
    let imagesSelect = document.querySelector("#new-item-img");
    for(let image in foodImgs){
        let option = document.createElement("option");
        // Assign value and innerHTML
        option.value = image;
        option.innerHTML = image;
        imagesSelect.appendChild(option);
    }
}

function showLoadingIcon(attachTo) {
    let loadingIcon = document.createElement("p");
    loadingIcon.classList.add("loading-icon");
    loadingIcon.innerHTML = "";

    // Appedn on page
    attachTo.parentNode.appendChild(loadingIcon);
    let percentage = 0;
    setInterval(() => {
        percentage += 20;
        if(percentage <= 100){
            loadingIcon.innerHTML = `loading ... ${percentage}%`;
        }
    }, 1000);
}

let inCart = [];


function flashMessage(hideOthers, showConfirmBtn, msg) {
    let messageP = document.createElement("p");
    messageP.id = "flash-message-p";
    messageP.classList.add("msg-paragraph");
    messageP.classList.add("flash-message");

    let spanWithMessage = document.createElement("span");
    spanWithMessage.id = "flash-span";
    
    spanWithMessage.innerHTML = msg;
    messageP.appendChild(spanWithMessage);

    // Append on page
    document.querySelector("body").appendChild(messageP);

    if(hideOthers){
        // Attachh close btn
        messageP.appendChild(closeBtn);
        for(let tag of [footer, section]){
            tag.classList.add("hidden-mode");
        }
    }
    else {
        for(let tag of [footer, section]){
            tag.classList.remove("hidden-mode");
        }
    }
    if(showConfirmBtn){
        // Append a `Yes` btn
        let yesBtn = closeBtn.cloneNode();
        yesBtn.innerHTML = "Yes";
        yesBtn.id = "yes-btn";
        yesBtn.classList.add("confirm-btn-full");

        messageP.appendChild(closeBtn);
        messageP.appendChild(yesBtn);

        for(let btn of [closeBtn, yesBtn]){
            // Add click listeners
            btn.addEventListener("click", () => {
                if(btn.innerHTML === "Yes"){
                    return true;
                }
                else if(btn.innerHTML === "Close"){
                    return false;
                }
            });
        }
    }  
}