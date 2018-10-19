// Consume API here
'use strict'; // Use ES6

// Icons
let acceptIcon = `<i class="far fa-check-circle"></i>`;
let rejectIcon = `<i class="far fa-times-circle"></i>`;
let deleteIcon = `<i class="fas fa-trash-alt"></i>`;
let completeIcon = `<i class="fas fa-check-double"></i>`;


// Select ol with order items
let ordersOL = document.querySelector("#in-cart");
let ordersDiv = document.querySelector("#orders-div");

// select logout button
let logoutBtn = document.querySelector("#logout-link");
const section = document.querySelector('section');

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
        // Remove close btn on error div
        responseDiv.lastChild.remove();
        showResponseMessage(ordersDiv, `Please <a class="adm-login-link" href="auth/login.html">login as admin here.</a>
        <br><br><a class="adm-login-link" href="/">Homepage</a>`);
        logoutBtn.style.display = "None";
        document.querySelector("#edit-menu-link").style.display = "None";
    }
});


// Append responseDiv to page
// Defined in common_funcs.js
ordersDiv.parentNode.insertBefore(responseDiv, ordersDiv);
// Hide since it currently is empty
responseDiv.classList.add("hidden-mode");

// Add click listener
addClickListener(closeBtn);

function fetchOrders() {
    fetch(`${api_url}/orders`, {
        headers: {
            "Authorization": `Bearer ${adminToken}`
        }
    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        
        message = responseJSON.message;
        if(message === "No orders yet.") {
            // Show message
            showMessageIfNoItems(ordersOL, message);
            // Hide orders header
            document.querySelector("#orders-header").classList.add("hidden-mode");
        }
        else if(message === "Orders found.") {
            
            // Add every user here to be used as filter option
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
                let orderedBy = order.ordered_by;
                orderByP.innerHTML = orderedBy;
          
                // Add ordered_by to filter options, if not already there
                if(filterOptions.indexOf(orderedBy) < 0) {
                  filterOptions.push(orderedBy);
                }
                
                // Attach p's to parent
                [orderedOnP, orderByP].forEach(infoP => {
                    appendToparent(infoP, timestampSpan);
                });

                // Attach spans to parent div
                [metaInfoSpan, orderInfoSpan, orderTotalSpan, timestampSpan].forEach(span => {
                    appendToparent(span, orderInfoDiv);
                });

                // Add order reation buttons
                let reactionsP = document.createElement("p");
                reactionsP.classList.add("order-rxn-btns");

                // Accept or Complete btn
                let acceptBtn = document.createElement("button");
                acceptBtn.classList.add("accept-order");
                // Append a default icon
                acceptBtn.innerHTML = acceptIcon;
                // Add an appropriate tootlip
                acceptBtn.setAttribute("title", "Accept Order");

                // Reject or Delete btn
                let rejectBtn = document.createElement("button");
                rejectBtn.classList.add("reject-order");
                rejectBtn.innerHTML = rejectIcon;
                rejectBtn.setAttribute("title", "Reject Order");

                // Attach btns to parent p
                [acceptBtn, rejectBtn].forEach(btn => {
                    btn.classList.add("order-reactions");
                    appendToparent(btn, reactionsP);

                    // Add click listeners
                    addClickListener(btn);

                });
                // Assign right icon depending on status
                assignIconByStatus([acceptBtn, rejectBtn], orderStatus);

                // Append all the things to parent li
                [orderInfoDiv, reactionsP].forEach(tag => {
                    appendToparent(tag, orderLi);
                });

                // Append li to parent ol
                appendToparent(orderLi, ordersOL);

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
            showResponseMessage(ordersDiv, message);
        }
        else {            
            let orderInfo = responseJSON.order.order_info;
            orderId = responseJSON.order.order_id;
            orderStatus = responseJSON.order.order_status;
            let orderCost = responseJSON.order.total_order_cost;
            let orderedBy = responseJSON.order.ordered_by;
            showResponseMessage(ordersDiv, `${message}<br>Status Updated Successfully<br><p class="order-summary">The order <br><br> order ID: ${orderId}<br>order Status: ${orderStatus}<br>order Summary: ${orderInfo}<br>Total cost: Ksh. ${orderCost}<br><br>Ordered by: ${orderedBy}<br></p>`);
        } 
    })
    .catch(error => {
        console.log(error);
    });
}


function deleteOrder(orderId) {
    // Delete Order
    fetch(`${api_url}/orders/${orderId}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${adminToken}`
        }
    })
    .then(response => response.json())
    .then(responseJSON => {
        let message = responseJSON.message;
        showResponseMessage(ordersDiv, message);
    })
    .catch(error => {
        console.log(error);
    });
}



function addClickListener(btn) {
    let orderStatus;
    btn.addEventListener("click", (event) => {
        // Find id of clicked order
        let clickedOrder = btn.parentNode.parentNode;
        let clickedOrderID = clickedOrder.querySelector("p.order-id").innerHTML.split("#")[1];

        if([acceptIcon, rejectIcon, completeIcon].indexOf(btn.innerHTML) > -1) {

            // Set status as appropriate
            if(btn.innerHTML === acceptIcon){
                // Send order status
                orderStatus = "Processing";
            }
            else if(btn.innerHTML === rejectIcon) {
                orderStatus = "Cancelled";
            }
            else if(btn.innerHTML === completeIcon) {
                orderStatus = "Complete";
            }

            // Call update order fn with params
            updateOrderStatus(clickedOrderID, orderStatus);
        }

        else if(btn.innerHTML === "Close") {
            // Refresh page
            window.location.replace("orders.html");
        }

        else if(btn.innerHTML === deleteIcon) {
            // Call delete function
            deleteOrder(clickedOrderID);
        }

    });
}


function assignIconByStatus(buttons, orderStatus) {
    if(orderStatus === "Cancelled") {
        // If order was Cancelled, provide only Delete icon
        buttons[0].style.display = "None";
        buttons[1].classList.add("delete-order");
        buttons[1].innerHTML = deleteIcon;
        // Assign an appropriate tooltip
        buttons[1].setAttribute("title", "Delete order");
    }
    else if(orderStatus === "Processing") {
        // For accepted order, provide only option to Mark Complete
        buttons[1].style.display = "None";
        buttons[0].classList.add("mark-complete");
        buttons[0].innerHTML = completeIcon;
        buttons[0].setAttribute("title", "Mark Complete");
    }
    else if(["Complete", "Deleted"].indexOf(orderStatus) > -1) {
        // Hide action btns for a deleted or completed order
        buttons[0].style.display = "None";
        buttons[1].style.display = "None";
    }
}