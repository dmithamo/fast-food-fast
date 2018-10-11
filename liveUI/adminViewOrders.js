// Consume API here
'use strict'; // Use ES6

const api_url = "https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2";


// loginResp
let adminToken = localStorage.adminToken;
let loggedInSince = localStorage.loggedInSince;

// Reusable variable
let message = '';


// Select ol with order items
let ordersOL = document.querySelector("#in-cart");

// select logout button
let logoutBtn = document.querySelector("#logout-link");


// Remove admin token on logout 
logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("adminToken");
    message = "Please login";
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

                // meta-info span with 2 p tags
                let metaInfoSpan = document.createElement("span");
                metaInfoSpan.classList.add("meta-info");

                // meta info: first p-tag
                let orderStatusP = document.createElement("p");
                orderStatusP.classList.add("order-status");
                orderStatusP.innerHTML = `[ #${order.order_status} ]`;

                // meta info: second p-tag
                let orderByP = document.createElement("p");
                orderByP.classList.add("ordered-by");
                orderByP.innerHTML = order.ordered_by;
                
                // Attach p's to parent
                [orderStatusP, orderByP].forEach(orderP => {
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


// On document ready
document.addEventListener('DOMContentLoaded', () => {
    if(adminToken){
        fetchOrders();
    }
    else {
        showMessageIfNoOrders(`Please <a class="adm-login-link" href="login.html">login as admin here.</a>`);
    }
});
