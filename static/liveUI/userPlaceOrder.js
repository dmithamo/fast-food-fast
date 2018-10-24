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
menuDiv.parentNode.insertBefore(responseDiv, menuDiv);
// Hide since it currently is empty
responseDiv.classList.add("hidden-mode");


// select logout button
let logoutBtn = document.querySelector("#logout-link");

// Remove user token on logout 
logoutBtn.addEventListener("click", () => {
    localStorage.clear();
});

// On page load
document.addEventListener('DOMContentLoaded', () => {
    if(!userToken) {
        responseDiv.lastChild.remove();
        showResponseMessage(menuDiv, `Please <a class="login-link" href="../auth/login.html">login</a> or <a class="login-link" href="../auth/register.html">register</a>`);
        // Change text in logout link
        document.querySelector("#logout-link").innerHTML = "Homepage";
        // Hide order history button
        document.querySelector("#history-link").style.display = "None";
        // Hide menu and menu header
        menuUL.classList.add("hidden-mode");

        // Hide shopping cart
        let shoppingCart = menuDiv.nextElementSibling;
        shoppingCart.classList.add("hidden-mode");

        // Display section as blok instead of grid
        document.querySelector("section.user-menu").style.display = "block";
    }
    else {
        // Wait a while for all menu to load
        setTimeout(() => {
            // Display logged in name
            document.querySelector("#logged-in-as").innerHTML = `[ ${loggedInAs} ]`;
            // Add order btns to each menu item
            addOrderBtns();

            // Populate cart with items in cart, if any
            populateCart();

        }, 1500);
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
        // Extract foodId of clicked menu item, and Price and Name
        let foodId = +window.clickedMenuItem.querySelector("p.food-id").innerHTML.split("#")[1];

        btn.addEventListener("click", () => {
            // Extract quantity
            let quantityInput = quantityModal.querySelector("#q-input-number");
            let quantity = +quantityInput.value;
            if(quantity){
                // Make POST request to server, if quantity is > 0
                addToCart(quantity, clickedMenuItem);
                window.location.replace("place_order.html");
            }
            else {
                // Show error
                warningWrongValue.innerHTML = "Quantity cannot be 0 or greater that 5!";
                quantityInput.parentNode.insertBefore(warningWrongValue, btn);
                highlightWrongInputOnForm("Quantity ...");

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
    quantityModal.classList.remove("wrong-input");
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
            // Hide order creation div
            hideQuantityModal();
            // Show order info
            showResponseMessage(menuDiv, `${message}<br><br><p class="order-summary">The order <br><br> order ID: ${orderId}<br>order Status: ${orderStatus}<br>order Summary: ${orderInfo}<br>Total cost: Ksh. ${orderCost}<br><br>Ordered by: ${orderedBy}<br></p>`);
        }
        else {
            // Show message
            warningWrongValue.innerHTML = message;
            foodItemName.parentNode.insertBefore(warningWrongValue, foodItemName.nextSibling);
            highlightWrongInputOnForm(message);
        }

        })
    .catch(function(error) {
        console.log(error);
    });
}

function addToCart(quantity, clickedMenuItem) {
    // Extract name, price and id of clickedMenuItem

    let foodId = +window.clickedMenuItem.querySelector("p.food-id").innerHTML.split("#")[1];
    let foodName = window.clickedMenuItem.querySelector("p.item-name").innerHTML;
    let foodPrice = +window.clickedMenuItem.querySelector("p.item-price").innerHTML.split(" ")[1];

    // Check if item is already in cart
    if(`order${foodId}` in localStorage){
        alert("Already in cart");
        let theItem = JSON.parse(localStorage[`order${foodId}`]);
        let currentQ = +theItem["quantity"];

        // Update quantity and save
        localStorage.setItem(`order${foodId}`, JSON.stringify(
            {"foodId": `${foodId}`, "foodName": `${foodName}`, "foodPrice": `${foodPrice}`, "quantity": `${quantity + currentQ}`}
        ));

    }
    else {
        localStorage.setItem(`order${foodId}`, JSON.stringify(
            {"foodId": `${foodId}`, "foodName": `${foodName}`, "foodPrice": `${foodPrice}`, "quantity": `${quantity}`}
            ));
    }

}


function populateCart() {
    // localStorage
    let numberOfItems = 0;
    for(let item in localStorage){
        if(localStorage.hasOwnProperty(item)){
            if(item.slice(0, 5) === "order"){
                
                // Display number of items in cart
                numberOfItems += 1;
                document.querySelector("#number-items").innerHTML = ` ${numberOfItems} `;

                let li = JSON.parse(localStorage[item]);

                // Extract params
                let foodId = li["foodId"];
                let foodName = li["foodName"];
                let foodPrice = li["foodPrice"];
                let quantity = li["quantity"];

                // Append item to cart as li
                let newOrderLi = document.createElement("li");
                newOrderLi.classList.add("new-cart-item");

                // Create a span for foodId, name, price, quantity and totalcost
                let idSpan = document.createElement("span");
                idSpan.innerHTML = `#00${foodId}`;

                let nameSpan = document.createElement("span");
                nameSpan.innerHTML = foodName;

                let priceSpan = document.createElement("span");
                priceSpan.innerHTML = +foodPrice;

                let quantitySpan = document.createElement("span");
                quantitySpan.innerHTML = +quantity;

                let totalCostSpan = document.createElement("span");
                totalCostSpan.innerHTML = foodPrice * quantity;

                for(let span of [idSpan, nameSpan, priceSpan, quantitySpan, totalCostSpan]){
                    span.classList.add("cart-span");
                    newOrderLi.appendChild(span);
                }
                document.querySelector("#in-cart").appendChild(newOrderLi);
            }
        }
    }
}