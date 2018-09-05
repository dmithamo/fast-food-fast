'use strict'; // Enable ES^ Features

// Select reusable elements from document
const listOfOrdersInCart = document.getElementById('in-cart');
const listOfOrdersInHistory = document.getElementById('in-history');
const confirmOrderBtn = document.getElementById('confirm-order-btn');
const numberDisplay = document.getElementById('number-items');
const orderHistoryLink = document.querySelector('#history-link');
const addNewFoodBtn = document.querySelector('#add-new-food');
const saveNewFood = document.querySelector('#save-new-btn')

document.addEventListener('DOMContentLoaded', () => {
    // Add click listeners to all order btns
    addBtnClickListeners();
    addConfirmOrderClickListener();
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
    };

    if (addNewFoodBtn) {
        addNewFoodBtn.addEventListener('click', () => {
            addNewFoodItem();
        });
    };

    if (saveNewFood) {
        saveNewFood.addEventListener('click', () => {
            saveFoodItem();
        });
    };
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
    
    // Append a copy to history
    const orderCopy = orderToAppend.cloneNode(true);
    listOfOrdersInHistory.appendChild(orderCopy);

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
};

function adminModifyItem(item) {
    // Modify an item on the list
    // Edit image src attribute
    const imgSrc = item.querySelector('img').getAttribute('src');
    const newImgSrc = prompt('Update image url to?', imgSrc);
    if (newImgSrc && newImgSrc !== imgSrc) {
        item.querySelector('img').setAttribute('src', newImgSrc);
    };

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
    // On initial click 
    if (orderHistoryLink.innerHTML === 'Order History') {
        // Change text of link
        orderHistoryLink.innerHTML = 'Back';
        // Hide list of food items and Shopping cart
        document.querySelector('#food-items').style.display = 'none';
        document.querySelector('#shopping-cart').style.display = 'none';
        // Show history cart
        document.querySelector('#history-cart').style.display = 'inline';
        // Hide misbehaving footer
        document.querySelector('footer').style.display = 'none';
    }
    // Chnage back everything
    else if (orderHistoryLink.innerHTML === 'Back') {
        // Change text of link
        orderHistoryLink.innerHTML = 'Order History';
        // Hide list of food items and Shopping cart
        document.querySelector('#food-items').style.display = 'inline';
        document.querySelector('#shopping-cart').style.display = 'inline';
        // Show history cart
        document.querySelector('#history-cart').style.display = 'none';
        // Hide misbehaving footer
        document.querySelector('footer').style.display = 'inline';
    }
};

function addNewFoodItem() {
    // Respond to click event on add-new-food btn
    // Display editing form and hide other items
    toggleEditingMode();

    // Create and style new food item as li
    window.newFoodItem = document.createElement('LI');
    newFoodItem.classList.add('food-item');

    const foodItemMarkUp = '<figure>' +
            '<img src="" alt="new-item">' +
            '<figcaption>' +
                '<p class="item-name"></p>' +
                '<p class="item-price"></p>' +
                '<button class="admin-btn edit-btn">Modify</button>' +
                '<button class="admin-btn delete-btn">Delete</button>' +
            '</figcaption>' +
        '</figure>'
    
    newFoodItem.innerHTML = foodItemMarkUp
};

function saveFoodItem() {
    // Save on btn click
    // Modify img src
    // Retrieve value of the img url input
    const newItemSrc = document.querySelector('#new-img-url').value;
    // Update food item img
    newFoodItem.querySelector('figure').querySelector('img').setAttribute('src', newItemSrc);
    // Modify food name
    // Retrieve value of the food name from input
    const newItemName = document.querySelector('#new-item-name').value;
    // Update food item name
    newFoodItem.querySelector('figure').querySelector('figcaption').querySelector('.item-name').innerHTML = newItemName;
    // Modify food price
    // Retrieve value of the food price from input
    const newItemPrice = document.querySelector('#new-item-price').value;
    // Update food item name
    newFoodItem.querySelector('figure').querySelector('figcaption').querySelector('.item-price').innerHTML = `Ksh. ${newItemPrice}.00`;
    
    // Append newFoodItem
    const foodItemsList = document.querySelector('#food-items');
    foodItemsList.appendChild(newFoodItem);
    addClickListenersToAdminBtns();

    // Hide editing form and reveal rest of page
    toggleEditingMode();
}


function toggleEditingMode() {
    const editingForm = document.querySelector('#editing-modal');
    const section = document.querySelector('section');
    const footer = document.querySelector('footer');

    const elements = [editingForm, section, footer];

    for (let elem of elements) {
        elem.classList.toggle('hidden-mode');
    }
};