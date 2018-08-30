'use strict'; // Enable ES^ Features

// Select reusable elements from document
const listOfOrdersInCart = document.getElementById('in-cart');
const confirmOrderBtn = document.getElementById('confirm-order-btn');
const numberDisplay = document.getElementById('number-items');

document.addEventListener('DOMContentLoaded', () => {
    // Add click listeners to all order btns
    addOrderBtnClickListeners();
    addConfirmOrderClickListener();
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

function addConfirmOrderClickListener() {
    confirmOrderBtn.addEventListener('click', () => {
        const number = listOfOrdersInCart.querySelectorAll('li').length;
        if (number > 0) {
            confirmOrder();
        }
        else {
            alert('You have not placed any orders yet.');
        }
    });
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

    // Update number in cart
    updateNumberInCart();
};

function updateNumberInCart() {
    const numberInCart = listOfOrdersInCart.querySelectorAll('li').length;
    // Update number in cart display
    numberDisplay.innerHTML = numberInCart;

    // If number > 0, activate confirm btn
    if (numberInCart > 0) {
        // Activate confirm-order btn
        confirmOrderBtn.classList.remove('confirm-btn-empty');
    }
};

function confirmOrder() {
    alert('Your order has been recieved!');
    // Clear list of orders
    listOfOrdersInCart.innerHTML = '';
    // Update number in cart display
    numberDisplay.innerHTML = 0;
    // Deactivate confirm-order btn
    confirmOrderBtn.classList.add('confirm-btn-empty');
};