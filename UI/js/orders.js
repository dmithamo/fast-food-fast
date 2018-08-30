'use strict'; // Enable ES^ Features

// Select reusable elements from document
const listOfOrdersInCart = document.getElementById('in-cart');
const confirmOrderBtn = document.getElementById('confirm-order-btn');
const numberDisplay = document.getElementById('number-items');

document.addEventListener('DOMContentLoaded', () => {
    // Add click listeners to all order btns
    addOrderBtnClickListeners();

});


function addOrderBtnClickListeners() {
    const orderBtns = document.querySelectorAll('.order-btn');
    // Add click listeners
    for (const orderBtn of orderBtns) {
        orderBtn.addEventListener('click', () => {
            //append clicked order to cart
            const parentOrder = orderBtn.parentElement.parentElement;
            appendOrderToCart(parentOrder);
        });
    }
};

function testSelections(list) {
    // Remember to remove. 
    for (const item of list) {
        alert(item.innerHTML);
    };
};

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

    // Determine number of orders so far made and update display
    determineNumberInCart();
};

function determineNumberInCart() {
    const numberInCart = listOfOrdersInCart.querySelectorAll('li').length;
    // Update number in cart display
    updateNumberInCart(numberInCart);
    return numberInCart;
}

function updateNumberInCart(number) {
    // Update number in cart display
    numberDisplay.innerHTML = number;

    // If number > 0, activate confirm btn
    if (number > 0) {
        // Select confirm-order btn
        confirmOrderBtn.classList.remove('confirm-btn-empty');
        // React to a click on confirm-order btn
        confirmOrderBtn.addEventListener('click', () => {
            confirmOrder();
        });
    }
};

function confirmOrder() {
    const number = determineNumberInCart();
    if (number > 0 ){
        alert('Your order has been recieved!');
    // Clear list of orders
    while (listOfOrdersInCart.firstChild) {
        listOfOrdersInCart.removeChild(listOfOrdersInCart.firstChild);
    };
    // Update number in cart display
    numberDisplay.innerHTML = 0;

    // Deactivate confirm-order btn
    confirmOrderBtn.classList.add('confirm-btn-empty')
    }
    else {
        alert('You have not added anything to your cart');
    }
}