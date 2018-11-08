// Consume API here
'use strict'; // Use ES6


// loginResp
let userToken = localStorage.userToken;
let loggedInAs = localStorage.loggedInAs;

// Reusable variables
let quantityModal = document.querySelector("#quantity-modal");
let deleteIcon = `<i class="fas fa-trash-alt"></i>`;


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
    for(let stored in localStorage){
        localStorage.removeItem(stored);
    }
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
            // Extract foodId of clicked menu item, and Price and Name
            let foodId = +window.clickedMenuItem.querySelector("p.food-id").innerHTML.split("#")[1];

            // Check if item is already in cart
            if(`order${foodId}` in localStorage){
                let updateQuantity = confirm(`This item is already in your cart. Would you like to update the quantity?`);
                if(updateQuantity){
                    let theItem = JSON.parse(localStorage[`order${foodId}`]);
                    let currentQ = +theItem["quantity"];
                    
                    // Show quantityDiv with current quantity
                    showQuantityModal(window.clickedMenuItem, currentQ);
                }
                else {
                    // alert("You said no");
                }
            }
            else {
                showQuantityModal(window.clickedMenuItem);
            }


        });
    }

    // Save btn
    if(btn.value === "Place order") {
        btn.addEventListener("click", () => {
            // Extract quantity
            let quantityInput = quantityModal.querySelector("#q-input-number");
            let quantity = +quantityInput.value;
            if(quantity){
                // Add item to Cart, if quantity is > 0
                addToCart(quantity, clickedMenuItem);
                
                // Hide quantity div
                hideQuantityModal();
                setTimeout(() => {
                    location.reload();
                }, 1000);
            }
            else {
                // Show error
                warningWrongValue.innerHTML = "Quantity cannot be 0!";
                quantityInput.parentNode.insertBefore(warningWrongValue, btn);
                highlightWrongInputOnForm("Quantity ...");
            }
        });
    }

    // Close or Cancel btn
    if(btn.innerHTML === "Close" || btn.value === "Cancel") {
        btn.addEventListener("click", () => {
            location.reload();
        });
    }

    // Confirm Order btn
    if(btn.innerHTML === "Confirm Order") {
        btn.addEventListener("click", () => {
            // Call placeOrder function for each item in the cart
            let itemsInCart = document.querySelectorAll("#in-cart>li");

            for(let item of itemsInCart){
                let foodId = +item.querySelector("span.food-id-span").innerHTML.split(" ")[1];
                let quantity = +item.querySelector("span.quantity-span").innerHTML;
                
                // Place order for each item
                placeOrder(foodId, quantity);
            }
            // Clear cart
            for(let item in localStorage){
                if(item.slice(0, 5) === "order"){
                    localStorage.removeItem(item);
                }
            }

            flashMessage(true, `Orders successfully placed.<br><br><a class="adm-login-link" href="view_orders.html">Track Progress</a><br><br><br>`);
        });
    }

    // Delete btn (from cart)
    if(btn.innerHTML === deleteIcon){
        btn.addEventListener("click", () => {
            // Id the clicked food item
            let clickedItem = btn.parentNode.parentNode;
            let foodId = clickedItem.querySelector(".food-id-span").innerHTML.split(" ")[1];
            // Remove from local storage
            localStorage.removeItem(`order${foodId}`);
            // Reload page
            flashMessage(false, "Removing ...");
            setTimeout(() => {
                location.reload();
            }, 1500);
        });
    }
}

function showQuantityModal(clickedMenuItem, quantity=0) {
    // Name of food
    let searchTerm = clickedMenuItem.querySelector("p.item-name").innerHTML;
    for(let tag of [section, footer]) {
        tag.classList.add('hidden-mode');
    }

    // Append name to quantity modal
    quantityModal.querySelector("span#q-food-name").innerHTML = ` ${searchTerm}s`;

    // Append quantity, if any
    if(quantity){
        quantityModal.querySelector("#q-input-number").value = quantity;
    }

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
    .then((response)=> {
        if(response.status < 500){
            return response.json()
        }
        else{
            location.replace('error_page')
        }
    })
    .then(function(responseJSON) {
        message = responseJSON.message;
        if(message === "Order posted successfully") {
            // Hide order creation div
            hideQuantityModal();
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
        window.location.replace("../error_page");
    });
}

function addToCart(quantity, clickedMenuItem) {
    // Extract name, price and id of clickedMenuItem

    let foodId = +window.clickedMenuItem.querySelector("p.food-id").innerHTML.split("#")[1];
    let searchTerm = window.clickedMenuItem.querySelector("p.item-name").innerHTML;
    let foodPrice = +window.clickedMenuItem.querySelector("p.item-price").innerHTML.split(" ")[1];

    localStorage.setItem(`order${foodId}`, JSON.stringify(
        {"foodId": `${foodId}`, "searchTerm": `${searchTerm}`, "foodPrice": `${foodPrice}`, "quantity": `${quantity}`}
        ));
}


function populateCart() {
    // localStorage
    let numberOfItems = 0;
    let totalCost = 0;
    for(let item in localStorage){
        if(localStorage.hasOwnProperty(item)){
            if(item.slice(0, 5) === "order"){
                
                // select cart
                let cart = document.querySelector("#in-cart");

                // Display number of items in cart
                numberOfItems += 1;
                document.querySelector("#number-items").innerHTML = ` ${numberOfItems} `;

                let li = JSON.parse(localStorage[item]);

                // Extract params
                let foodId = li["foodId"];
                let searchTerm = li["searchTerm"];
                let foodPrice = li["foodPrice"];
                let quantity = li["quantity"];

                // Append item to cart as li
                let newOrderLi = document.createElement("li");
                newOrderLi.classList.add("new-cart-item");

                // Create a span for foodId, name, price, quantity and totalcost, and deleteIcon
                let idSpan = document.createElement("span");
                idSpan.innerHTML = `#00 ${foodId}`;
                idSpan.classList.add("food-id-span");

                let nameSpan = document.createElement("span");
                nameSpan.innerHTML = searchTerm;

                let priceSpan = document.createElement("span");
                priceSpan.innerHTML = +foodPrice;

                let quantitySpan = document.createElement("span");
                quantitySpan.innerHTML = +quantity;
                quantitySpan.classList.add("quantity-span");

                let totalCostSpan = document.createElement("span");
                let totalPerItem = foodPrice * quantity;
                totalCost += totalPerItem;
                totalCostSpan.innerHTML = totalPerItem;

                let deleteSpan = document.createElement("span");
                deleteSpan.id = "delete-from-cart";
                deleteSpan.innerHTML = deleteIcon;
                addClickListener(deleteSpan);

                for(let span of [idSpan, nameSpan, priceSpan, quantitySpan, totalCostSpan, deleteSpan]){
                    span.classList.add("cart-span");
                    newOrderLi.appendChild(span);
                }
                cart.appendChild(newOrderLi);
            }
        }
    }
    // Activate confirm btn and show total if numberOfItems > 0
    if(numberOfItems > 0){
        // Confirm btn
        let confirmBtn = document.querySelector("#confirm-order-btn");
        confirmBtn.classList.remove("confirm-btn-empty");
        addClickListener(confirmBtn);

        // Show all of Cart
        document.querySelector("#cart-params").classList.remove("hidden-mode");

        // Update total
        let totalDisp = document.querySelector("#cart-footer");
        totalDisp.innerHTML = `Total Cost : Kshs. ${totalCost}`;

    }

}

let searchBar = document.querySelector("#search-input")
searchBar.addEventListener('keyup', () => {
    searchFoodItem();
})

function searchFoodItem(){

    // Query for a meal with agiven name
    let foodFound = false;
    let searchTerm = searchBar.value.toLowerCase();
    // See if name of any of the items on menu matches searchTerm
    let allFoods = document.querySelectorAll(".item-name");
    for(let name of allFoods){
        let parentLi = name.parentNode.parentNode.parentNode;
        let foodItemName = name.innerHTML.toLowerCase();
        if(!foodItemName.includes(searchTerm)){
            parentLi.classList.add("hidden-mode");
        }
        if(foodItemName.includes(searchTerm)){
            parentLi.classList.remove("hidden-mode");
            foodFound = true;
        }
    }

    // Display message if no match
    let messagePara = document.querySelector("#search-empty");
    if(!foodFound) {
        messagePara.innerHTML = "Nothing found! :( Try tweaking the search term a bit";
    } else {
        messagePara.innerHTML = "";

    }

}