// Consume API here
'use strict'; // Use ES6


// loginResp
let userToken = localStorage.userToken;
let loggedInAs = localStorage.loggedInAs;

// Reusable variables
let message = '';
const section = document.querySelector('section');
const footer = document.querySelector('footer');
let quantityModal = document.querySelector("#quantity-modal");


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
// Add click listener
addClickListener(closeBtn);


// Append to page
menuUL.parentNode.parentNode.insertBefore(errorDiv, menuUL.parentNode);
// Hide since it currently is empty
errorDiv.classList.add("hidden-mode");


// select logout button
let logoutBtn = document.querySelector("#logout-link");

// Remove user token on logout 
logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("userToken");
    localStorage.removeItem("loggedInAs");
});

// On page load
document.addEventListener('DOMContentLoaded', () => {
    if(!userToken) {
        errorDiv.lastChild.remove();
        showMessageIfError(`Please <a class="login-link" href="../auth/login.html">login</a> or <a class="login-link" href="../auth/register.html">register</a>`);
        // Change text in logout link
        document.querySelector("#logout-link").innerHTML = "See Menu";
        // Hide order history button
        document.querySelector("#history-link").style.display = "None";
    }
    else {
        // Wait a while for all menu to load
        setTimeout(() => {
            // Display logged in name
            document.querySelector("#logged-in-as").innerHTML = `[ ${loggedInAs} ]`;
            // Add order btns to each menu item
            addOrderBtns();
        }, 500);
    }
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


function addOrderBtns() {
    // Select all menu item figcaptions
    let menuItemCaptions = document.querySelectorAll("figcaption");
    for(let item of menuItemCaptions) {
        // Appedn to each menu item an Add to Cart btn
        // Modify btn
        let addBtn = document.createElement("button");
        addBtn.classList.add("order-btn");
        addBtn.innerHTML = `Add to <i class="fas fa-shopping-basket"></i>`;

        // Attach btn
        item.appendChild(addBtn);

        // Set a click listener on btn
        addClickListener(addBtn);
    }
}

function addClickListener(btn) {
    let clickedMenuItem;

    // Add new btn
    if(btn.innerHTML === `Add to <i class="fas fa-shopping-basket"></i>`) {
        btn.addEventListener("click", () => {
            // Reveal editing modal on function call
            window.clickedMenuItem = btn.parentNode.parentNode.parentNode;
            showQuantityModal(window.clickedMenuItem);
        });
    }

    // Save btn
    if(btn.value === "Add to Cart") {
        // Extract foodId of clicked menu item
        let foodId = +window.clickedMenuItem.querySelector("p.food-id").innerHTML.split("#")[1];

        btn.addEventListener("click", () => {
            // Extract quantity
            let quantity = +quantityModal.querySelector("#q-input-number").value;
            // Make POST request to server
            placeOrder(foodId, quantity);
            // Hide editing modal
            hideQuantityModal();
        });
    }

    // Close or Cancel btn
    if(btn.innerHTML === "Close" || btn.value === "Cancel") {
        btn.addEventListener("click", () => {
            window.location.replace("orders.html");
        });
    }
}

function showQuantityModal(clickedMenuItem) {
    // Name of food
    let foodName = clickedMenuItem.querySelector("p.item-name").innerHTML;
    for(let tag of [section, footer]) {
        tag.classList.add('hidden-mode');
    }

    // Append name to quantity modal
    quantityModal.querySelector("span#q-food-name").innerHTML = ` ${foodName}s`;
    quantityModal.classList.remove("hidden-mode");
    // Add cick listeners to btns on modal
    let addQ = document.querySelector("#add-q-btn");
    let cancel = document.querySelector("#cancel-q-btn");

    for(let btn of [addQ, cancel]) {
        addClickListener(btn);
    }

}

function hideQuantityModal() {
    for(let tag of [section, footer]) {
        tag.classList.remove('hidden-mode');
    }
    quantityModal.classList.add("hidden-mode");
}

function placeOrder(foodId, quantity) {
    let data = {
        "food_item_id": foodId,
        "quantity": quantity
    };
    // POST menu item
    fetch(`${api_url}/users/orders`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${userToken}`
        }
    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        message = responseJSON.message;
        if(message === "Order posted successfully") {
            console.log(responseJSON);
            let orderInfo = responseJSON.order.order_info;
            let orderId = responseJSON.order.order_id;
            let orderCost = responseJSON.order.total_order_cost;
            let orderedBy = responseJSON.order.ordered_by;
            // Show order info
            showMessageIfError(`${message}<br><br><p class="order-summary">Your order <br><br> order ID: ${orderId}<br>order Summary: ${orderInfo}<br>Total cost: Ksh. ${orderCost}<br><br>Your name: ${orderedBy}</p>`);
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

function getOrderHistory(foodId) {
    // POST menu item
    fetch(`${api_url}/users/orders`, {
        method: 'GET',
        headers: {
            "Authorization": `Bearer ${adminToken}`
        }
    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        message = responseJSON.message;
        alert(message);
        if(message === "Orders found") {
            // Reload menu page
            window.location.replace("orders.html");
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
