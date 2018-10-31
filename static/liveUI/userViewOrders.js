// Consume API here
'use strict'; // Use ES6


// loginResp
let userToken = localStorage.userToken;
let loggedInAs = localStorage.loggedInAs;

// Select history link and history Div and menu Div
let placeOrderLink = document.querySelector("#place-order-link");
addClickListener(placeOrderLink);

// Select ol with order items
let ordersOL = document.querySelector("#in-cart");
let ordersDiv = document.querySelector("#orders-div");

// Add click listener
addClickListener(closeBtn);

// Append to page
ordersDiv.parentNode.insertBefore(responseDiv, ordersDiv);
// Hide since it currently is empty
responseDiv.classList.add("hidden-mode");

// select logout button
let logoutBtn = document.querySelector("#logout-link");
// Add click listener
addClickListener(logoutBtn);

// On page load
document.addEventListener('DOMContentLoaded', () => {
    if(!userToken) {
        responseDiv.lastChild.remove();
        showResponseMessage(ordersDiv, `Please <a class="login-link" href="../auth/login.html">login</a> or <a class="login-link" href="../auth/register.html">register</a>`);
        // Change text in logout link
        logoutBtn.innerHTML = "See Menu";
        // Hide order history button
        placeOrderLink.style.display = "None";
    }
    else {
        // Display logged in person
        document.querySelector("#logged-in-as").innerHTML = `[ ${loggedInAs} ]`;
        flashMessage(false, "Wait just one ...");
        setTimeout(() => {
            fetchOrders();
        }, 1000); 
    }
});

function fetchOrders() {
    fetch(`${api_url}/users/orders`, {
        method: 'GET',
        headers: {
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
        // Hide loading message
        document.querySelector("#flash-message-p").style.display = "None";

        // Analyse the response
        message = responseJSON.message;
        if(message === `No orders yet for user '${loggedInAs}'`) {
            showMessageIfNoItems(ordersOL, `You have not yet placed any orders.<br><br><a class="adm-login-link" href="place_order.html">Place Order</a>`);
            // Hide orders header
            document.querySelector("#orders-header").classList.add("hidden-mode");

        }
        else if(message === "Orders found.") {
            // Add every status here to be used as filter option
            let filterOptions = [];

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
                orderIdP.classList.add("order-id");
                orderIdP.innerHTML = `orderID#${order.order_id}`;

                // meta info: second p-tag
                let orderStatusP = document.createElement("p");
                orderStatusP.classList.add("order-status");
                let orderStatus = order.order_status;
                orderStatusP.innerHTML = `status: ${orderStatus}`;
          
                // Add ordered_by to filter options, if not already there
                if(filterOptions.indexOf(orderStatus) < 0) {
                  filterOptions.push(orderStatus);
                }
    

                // Style each order depending on status
                styleByStatus(orderLi, orderStatus);

                // meta info: third p-tag
                let statusAsAt = document.createElement("p");
                statusAsAt.classList.add("order-status");
                let correctedStatusTime = correctTime(order.status_update_on);
                statusAsAt.innerHTML = `[ as at: ${correctedStatusTime} ]`;
                
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
                let correctedOrderTime = correctTime(order.ordered_on);
                orderedOnP.innerHTML = `Placed On<br>${correctedOrderTime}`;

                // meta info: second p-tag
                let orderByP = document.createElement("p");
                orderByP.classList.add("ordered-by");
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
            // Add filter options on order history page
            addFilterOptions(filterOptions);

        }
        else {
            // Show message
            showResponseMessage(ordersDiv, message);
        }

        })
    .catch(function(error) {
        console.log(error);
        window.location.replace("../error_page");
    });
}


function addClickListener(btn) {

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
            window.location.replace("view_orders");
        });
    }
}

