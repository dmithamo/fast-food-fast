// Consume API here
'use strict'; // Use ES6


const api_url = "https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2";

// loginResp
let userToken = localStorage.userToken;
let loggedInAs = localStorage.loggedInAs;

// Reusable variables
let message = '';
const section = document.querySelector('section');
const footer = document.querySelector('footer');


// Select history link and history Div and menu Div
let placeOrderLink = document.querySelector("#place-order-link");
addClickListener(placeOrderLink);

// Select ol with order items
let ordersOL = document.querySelector("#in-history");


// Helper function
const appendToparent = (element, parent) => {
    parent.appendChild(element);
};

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
ordersOL.parentNode.insertBefore(errorDiv, ordersOL);
// Hide since it currently is empty
errorDiv.classList.add("hidden-mode");

// select logout button
let logoutBtn = document.querySelector("#logout-link");
// Add click listener
addClickListener(logoutBtn);

// On page load
document.addEventListener('DOMContentLoaded', () => {
    if(!userToken) {
        errorDiv.lastChild.remove();
        showMessageIfError(`Please <a class="login-link" href="../auth/login.html">login</a> or <a class="login-link" href="../auth/register.html">register</a>`);
        // Change text in logout link
        logoutBtn.innerHTML = "See Menu";
        // Hide order history button
        placeOrderLink.style.display = "None";
    }
    else {
        // Display logged in person
        document.querySelector("#logged-in-as").innerHTML = `[ ${loggedInAs} ]`;
        fetchOrders();
    }
});

function fetchOrders() {
    fetch(`${api_url}/users/orders`, {
        method: 'GET',
        headers: {
            "Authorization": `Bearer ${userToken}`
        }
    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        message = responseJSON.message;
        if(message !== "Orders found.") {
            // Show message
            showMessageIfError(message);
        }
        else {
            let orders = responseJSON.orders;
            orders.forEach(order => {
                // Create and style an li
                let orderLi = document.createElement("li");
                orderLi.classList.add("ordered-item");

                // Create and style constituent elements of the orderLi
                // Parent div
                let orderInfoDiv = document.createElement("div");
                orderInfoDiv.classList.add("the-order");

                // meta-info span with 3 p tags
                let metaInfoSpan = document.createElement("span");
                metaInfoSpan.classList.add("meta-info");

                // meta info: first p-tag
                let orderIdP = document.createElement("p");
                orderIdP.classList.add("order-status");
                orderIdP.classList.add("order-id");
                orderIdP.innerHTML = `orderID#${order.order_id}`;

                // meta info: second p-tag
                let orderStatusP = document.createElement("p");
                orderStatusP.classList.add("order-status");
                let orderStatus = order.order_status;
                orderStatusP.innerHTML = `[ status: ${orderStatus} ]`;

                // Style each order depending on status
                styleByStatus(orderLi, orderStatus);

                // meta info: third p-tag
                let statusAsAt = document.createElement("p");
                statusAsAt.classList.add("order-status");
                statusAsAt.innerHTML = `[ as at: ${order.status_update_on} ]`;
                
                // Attach p's to parent
                [orderIdP, orderStatusP, statusAsAt].forEach(orderP => {
                    appendToparent(orderP, metaInfoSpan);
                });

                // order-info span with 1 p tag
                let orderInfoSpan = document.createElement("span");

                // order-info: p-tag
                let orderInfoP = document.createElement("p");
                orderInfoP.classList.add("order-info");
                orderInfoP.innerHTML = order.order_info;

                // Attach p to parent
                appendToparent(orderInfoP, orderInfoSpan);

                // order-total span with 1 p-tag
                let orderTotalSpan = document.createElement("span");

                // order-total: p-tag
                let orderTotalP = document.createElement("p");
                orderTotalP.classList.add("order-total");
                orderTotalP.innerHTML = `Ksh. ${order.total_order_cost}`;

                // Attach p to parent
                appendToparent(orderTotalP, orderTotalSpan);
            
                // timestamp span with 2 p tags
                let timestampSpan = document.createElement("span");

                // timestamp: first p-tag
                let orderedOnP = document.createElement("p");
                orderedOnP.classList.add("timestamp");
                orderedOnP.innerHTML = `Placed On<br>${order.ordered_on}`;

                // meta info: second p-tag
                let orderByP = document.createElement("p");
                orderByP.classList.add("timestamp");
                orderByP.innerHTML = order.ordered_by;
                
                // Attach p's to parent
                [orderedOnP, orderByP].forEach(infoP => {
                    appendToparent(infoP, timestampSpan);
                });

                // Attach spans to parent div
                [metaInfoSpan, orderInfoSpan, orderTotalSpan, timestampSpan].forEach(span => {
                    appendToparent(span, orderInfoDiv);
                });

                // Append all the things to parent li
                appendToparent(orderInfoDiv, orderLi);

                // Append li to parent ol
                appendToparent(orderLi, ordersOL);

                // Style by order status
                styleByStatus(orderLi, orderStatus);

            });

        }

        })
    .catch(function(error) {
        console.log(error);
    });
}


const showMessageIfError = (message) => {
    // Show error message
    specialPara.innerHTML = message;
    // Hide everything else
    for(let tag of [ordersOL, footer]) {
        tag.classList.add("hidden-mode");
    }
    // Reveal errorDiv
    errorDiv.classList.remove("hidden-mode");
};

function addClickListener(btn) {

    // Place Order btn
    if(btn.innerHTML === "Place Order") {
        btn.addEventListener("click", () => {
            window.location.replace("place_order.html");
        });
    }

    // Logout btn
    if(btn.innerHTML === "Logout") {
        btn.addEventListener("click", () => {
            localStorage.removeItem("userToken");
            localStorage.removeItem("loggedInAs");
        });
    }

    // Close
    if(btn.innerHTML === "Close") {
        btn.addEventListener("click", () => {
            window.location.replace("view_orders.html");
        });
    }
}

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
}

