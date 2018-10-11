'use strict'; // Enable ES^ Features

// Select reusable elements from document
const listOfOrdersInCart = document.getElementById('in-cart');
const listOfOrdersInHistory = document.getElementById('in-history');
const confirmOrderBtn = document.getElementById('confirm-order-btn');
const numberDisplay = document.getElementById('number-items');
const orderHistoryLink = document.querySelector('#history-link');
const addNewFoodBtn = document.querySelector('#add-new-btn');
const saveNewFood = document.querySelector('#save-new-btn')

document.addEventListener('DOMContentLoaded', () => {
    // Add click listeners to all order btns
    addBtnClickListeners();
    // addConfirmOrderClickListener();
});


function addBtnClickListeners() {
    const orderBtns = document.querySelectorAll('.order-btn');
    // Add click listeners
    for (const orderBtn of orderBtns) {
        orderBtn.addEventListener('click', () => {
            //append clicked order to cart
            const parentOrder = orderBtn.parentElement.parentElement;
            appendOrderToCart(parentOrder);
        });
    }
    if (orderHistoryLink) {
        orderHistoryLink.addEventListener('click', () =>{
            showOrderHistory();
        });
    }

}


function appendOrderToCart(order) {
    // Extract order information
    const orderName = order.querySelector('.item-name').innerHTML;
    const orderPrice = order.querySelector('.item-price').innerHTML;
    const orderQuantity = 1;

    // Build out li with order info
    const orderInfo = `<div class="li-container"><span>${orderName}\
    </span><span class="order-quantity">x ${orderQuantity}</span><span \
    class="order-price">${orderPrice}</span></div>`;

    const orderToAppend = document.createElement("LI");
    orderToAppend.innerHTML = orderInfo;

    // Append li to ol of orders made
    listOfOrdersInCart.appendChild(orderToAppend);
    
    // Append a copy to history
    const orderCopy = orderToAppend.cloneNode(true);
    listOfOrdersInHistory.appendChild(orderCopy);

    // Update number in cart
    updateNumberInCart();
}

function updateNumberInCart() {
    const numberInCart = listOfOrdersInCart.querySelectorAll('li').length;
    // Update number in cart display
    numberDisplay.innerHTML = numberInCart;

    // If number > 0, activate confirm btn
    if (numberInCart > 0) {
        // Activate confirm-order btn
        confirmOrderBtn.classList.remove('confirm-btn-empty');
    }
}

function confirmOrder() {
    alert('Your order has been recieved!');
    // Clear list of orders
    listOfOrdersInCart.innerHTML = '';
    // Update number in cart display
    numberDisplay.innerHTML = 0;
    // Deactivate confirm-order btn
    confirmOrderBtn.classList.add('confirm-btn-empty');
}

// Admin functions
addClickListenersToAdminBtns();
reactToOrder();

function addClickListenersToAdminBtns() {
    // Respond to a click on Delete btn by admin
    const adminBtns = document.querySelectorAll('.admin-btn');
    for (const adminBtn of adminBtns) {
        adminBtn.addEventListener('click', () => {
            const parentItem = adminBtn.parentElement.parentElement.parentElement;
            if (adminBtn.innerHTML === 'Delete') {
                adminDeleteItem(parentItem);
            }
            else if (adminBtn.innerHTML === 'Modify') {
                adminModifyItem(parentItem);
            }
        });
    }
}

function adminModifyItem(item) {
    // Modify an item on the list
    // Edit image src attribute
    const imgSrc = item.querySelector('img').getAttribute('src');
    const newImgSrc = prompt('Update image url to?', imgSrc);
    if (newImgSrc && newImgSrc !== imgSrc) {
        item.querySelector('img').setAttribute('src', newImgSrc);
    }

    // Edit Name
    const nameOfItem = item.querySelector('figcaption').querySelector('.item-name').innerHTML;
    const newName = prompt('Update item name to?', nameOfItem);
    if (newName && newName !== nameOfItem) {
        item.querySelector('figcaption').querySelector('.item-name').innerHTML = newName;
    }

    // Edit price
    const priceOfItem = item.querySelector('figcaption').querySelector('.item-price').innerHTML;
    const newPrice = prompt('Update item price to?', priceOfItem);
    if (newName && newPrice !== priceOfItem) {
        item.querySelector('figcaption').querySelector('.item-price').innerHTML = newPrice;
    }

}

function adminDeleteItem(item) {
    // Delete item from list
    item.parentElement.removeChild(item);
};

function reactToOrder() {
    // Select reaction btns
    const reactionBtns = document.querySelectorAll('.order-reactions');
    for (const button of reactionBtns) {
        button.addEventListener('click', () => {
            const parentOrder = button.parentElement.parentElement;
            if (button.innerHTML === 'Accept Order') {
                parentOrder.classList.add('accepted-order');
                button.innerHTML = 'Mark Completed';
                button.nextElementSibling.style.display = 'none';
            }
            else if (button.innerHTML === 'Reject Order') {
                parentOrder.classList.add('rejected-order');
                button.innerHTML = 'Delete';
                button.previousElementSibling.style.display = 'none';
            }
            else if (button.innerHTML === 'Mark Completed') {
                parentOrder.classList.add('completed-order');
                button.innerHTML = 'Delete';
            }
            else if (button.innerHTML === 'Delete') {
                parentOrder.parentElement.removeChild(parentOrder);
            }
        });
    }

}

function showOrderHistory() {
    // Select elements
    const foodItems = document.querySelector('#food-items')
    const shoppingCart = document.querySelector('#shopping-cart');
    const historyCart = document.querySelector('#history-cart');
    const footer = document.querySelector('footer');
    // On initial click 
    if (orderHistoryLink.innerHTML === 'Order History') {
        // Change text of link
        orderHistoryLink.innerHTML = 'Back';
        // Hide list of food items and Shopping cart
        foodItems.style.display = 'none';
        shoppingCart.style.display = 'none';
        // Show history cart
        historyCart.style.display = 'inline';
        // Hide footer
        footer.style.display = 'none';
    }
    // Change back everything
    else if (orderHistoryLink.innerHTML === 'Back') {
        // Change text of link
        orderHistoryLink.innerHTML = 'Order History';
        // Show list of food items and Shopping cart
        foodItems.style.display = 'inline';
        shoppingCart.style.display = 'inline';
        // Hide history cart
        historyCart.style.display = 'none';
        // Show footer
        footer.style.display = 'block';
    }
}
