// Consume API here
'use strict'; // Use ES6


// loginResp
let userToken = localStorage.userToken;
let loggedInAs = localStorage.loggedInAs;

// Reusable variables
const section = document.querySelector('section');
// const footer = document.querySelector('footer');
let quantityModal = document.querySelector("#quantity-modal");


// Add click listener
addClickListener(closeBtn);


// Append to page
menuDiv.parentNode.insertBefore(errorDiv, menuDiv);
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
        showResponseMessage(menuDiv, `Please <a class="login-link" href="login">login</a> or <a class="login-link" href="register">register</a>`);
        // Change text in logout link
        document.querySelector("#logout-link").innerHTML = "Homepage";
        // Hide order history button
        document.querySelector("#history-link").style.display = "None";
        // Hide menu and menu header
        menuUL.classList.add("hidden-mode");
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
    if(btn.value === "Place order") {
        // Extract foodId of clicked menu item
        let foodId = +window.clickedMenuItem.querySelector("p.food-id").innerHTML.split("#")[1];

        btn.addEventListener("click", () => {
            // Extract quantity
            let quantityInput = quantityModal.querySelector("#q-input-number");
            let quantity = +quantityInput.value;
            if(quantity){
                // Make POST request to server, if quantity is > 0
                placeOrder(foodId, quantity);
                // Hide editing modal
                hideQuantityModal();
            }
            else {
                // Show error
                warningWrongValue.innerHTML = "Quantity cannot be 0 or greater that 5!";
                quantityInput.parentNode.insertBefore(warningWrongValue, btn);
            }
        });
    }

    // Close or Cancel btn
    if(btn.innerHTML === "Close" || btn.value === "Cancel") {
        btn.addEventListener("click", () => {
            window.location.replace("place_order.html");
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
            let orderInfo = responseJSON.order.order_info;
            let orderId = responseJSON.order.order_id;
            let orderStatus = responseJSON.order.order_status;
            let orderCost = responseJSON.order.total_order_cost;
            let orderedBy = responseJSON.order.ordered_by;
            // Show order info
            showResponseMessage(menuDiv, `${message}<br><br><p class="order-summary">The order <br><br> order ID: ${orderId}<br>order Status: ${orderStatus}<br>order Summary: ${orderInfo}<br>Total cost: Ksh. ${orderCost}<br><br>Ordered by: ${orderedBy}<br></p>`);
        }
        else {
            // Show message
            showResponseMessage(menuDiv, message);
        }

        })
    .catch(function(error) {
        console.log(error);
    });
}
