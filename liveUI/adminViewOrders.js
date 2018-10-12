// Consume API here
'use strict'; // Use ES6

const api_url = "https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2";


// loginResp
let adminToken = localStorage.adminToken;
let loggedInSince = localStorage.loggedInSince;

// Reusable variable
let message = '';
const footer = document.querySelector('footer');


// Select ol with order items
let ordersOL = document.querySelector("#in-cart");

// select logout button
let logoutBtn = document.querySelector("#logout-link");


// Remove admin token on logout 
logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("adminToken");
});

// On document ready
document.addEventListener('DOMContentLoaded', () => {
    if(adminToken){
        fetchOrders();
    }
    else {
        showMessageIfNoOrders(`Please <a class="adm-login-link" href="login.html">login as admin here.</a>`);
        logoutBtn.style.display = "None";
        document.querySelector("#edit-menu-link").style.display = "None";
    }
});

// Helper function
const appendToparent = (element, parent) => {
    parent.appendChild(element);
};

const showMessageIfNoOrders = (message) => {
    // Create and style a special paragraph to report that menu is empty
    let specialPara = document.createElement("p");
    specialPara.classList.add("msg-paragraph");
    specialPara.innerHTML = message;

    // Append to page
    ordersOL.parentNode.insertBefore(specialPara, ordersOL);
};

function fetchOrders() {
    fetch(`${api_url}/orders`, {
        headers: {
            "Authorization": `Bearer ${adminToken}`
        }
    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        message = responseJSON.message;
        if(message !== "Orders found.") {
            // Show message
            showMessageIfNoOrders(message);
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
                let orderByP = document.createElement("p");
                orderByP.classList.add("order-status");
                orderByP.innerHTML = order.ordered_by;
                
                // Attach p's to parent
                [orderIdP, orderStatusP, orderByP].forEach(orderP => {
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
                orderedOnP.innerHTML = "Placed On";

                // meta info: second p-tag
                let timeP = document.createElement("p");
                timeP.classList.add("timestamp");
                timeP.innerHTML = order.ordered_on;
                
                // Attach p's to parent
                [orderedOnP, timeP].forEach(timesP => {
                    appendToparent(timesP, timestampSpan);
                });

                // Attach spans to parent div
                [metaInfoSpan, orderInfoSpan, orderTotalSpan, timestampSpan].forEach(span => {
                    appendToparent(span, orderInfoDiv);
                });

                // Add order reation buttons
                let reactionsP = document.createElement("p");
                reactionsP.classList.add("order-rxn-btns");

                // Accept btn
                let acceptBtn = document.createElement("button");
                acceptBtn.classList.add("accept-order");
                acceptBtn.innerHTML = `<i class="far fa-check-circle"></i>`;

                // Reject btn
                let rejectBtn = document.createElement("button");
                rejectBtn.classList.add("reject-order");
                rejectBtn.innerHTML = `<i class="far fa-times-circle"></i>`;

                // Attach btns to parent p
                [acceptBtn, rejectBtn].forEach(btn => {
                    btn.classList.add("order-reactions");
                    appendToparent(btn, reactionsP);

                    // Add click listeners
                    addClickListener(btn);
                });

                // Append all the things to parent li
                [orderInfoDiv, reactionsP].forEach(tag => {
                    appendToparent(tag, orderLi);
                });

                // Append li to parent ol
                appendToparent(orderLi, ordersOL);

            });
        }

        })
    .catch(function(error) {
        console.log(error);
    });
}

function addClickListener(btn) {
    let orderStatus;
    btn.addEventListener("click", (event) => {
        // Find id of clicked order
        let clickedOrder = btn.parentNode.parentNode;
        let clickedOrderID = clickedOrder.querySelector("p.order-id").innerHTML.split("#")[1];

        // Set status as appropriate
        if(btn.innerHTML === `<i class="far fa-check-circle"></i>`){
            // Send order status
            orderStatus = "Processing";
        }
        else if(btn.innerHTML === `<i class="far fa-times-circle"></i>`) {
            orderStatus = "Cancelled";
        }
        else if(btn.innerHTML === "Close") {
            // Refresh page
            window.location.replace("orders.html");
        }

        // Call update order fn with params
        updateOrderStatus(clickedOrderID, orderStatus);

    });
}

function updateOrderStatus(orderId, orderStatus){
    fetch(`${api_url}/orders/${orderId}`, {
        method: 'PUT',
        body: JSON.stringify({
            "order_status": orderStatus
        }),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${adminToken}`
        }
    })
    .then(response => response.json())
    .then(function(responseJSON) {
        message = responseJSON.message;
        if(message !== "Order found.") {
            showMessageIfError(message);
        }
        else {            
            let orderInfo = responseJSON.order.order_info;
            orderId = responseJSON.order.order_id;
            orderStatus = responseJSON.order.order_status;
            let orderCost = responseJSON.order.total_order_cost;
            let orderedBy = responseJSON.order.ordered_by;
            showMessageIfError(`${message}<br>Status Updated Successfully<br><p class="order-summary">The order <br><br> order ID: ${orderId}<br>order Status: ${orderStatus}<br>order Summary: ${orderInfo}<br>Total cost: Ksh. ${orderCost}<br><br>Ordered by: ${orderedBy}<br></p>`);
            // Reload to reflect new styling
            setTimeout(() => {
                window.location.replace("orders.html");
            }, 3000);
        }
    })
    .catch(error => {
        console.log(error);
    });
}


// 

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

function styleByStatus(order, orderStatus){
    if(orderStatus === "New") {
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