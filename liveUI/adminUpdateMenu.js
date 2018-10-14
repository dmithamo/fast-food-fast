// Consume API here
'use strict'; // Use ES6


// Append to page
menuUL.parentNode.parentNode.insertBefore(errorDiv, menuUL.parentNode);
// Hide since it currently is empty
errorDiv.classList.add("hidden-mode");

// Select add-new-btn, editing-modal, save-btn, cancel-btn
let addNewBtn = document.querySelector("#add-new-btn");
let editingModal = document.querySelector("#editing-modal");
let saveNewBtn = document.querySelector("#save-new-btn");
let updateBtn = document.querySelector("#update-btn");
let cancelBtn = document.querySelector("#cancel-btn");
closeBtn = document.querySelector("#close-btn");

// collect btns in an array
let pageBtns = [addNewBtn, saveNewBtn, updateBtn, cancelBtn, closeBtn];

// select logout button
let logoutBtn = document.querySelector("#logout-link");

// Select footer, section, editing-modal to hide and show as necessary
const editingForm = document.querySelector('#editing-modal');
const section = document.querySelector('section');
// const footer = document.querySelector('footer');

// Collect new food item attributes
let foodItemName = document.querySelector("#new-item-name");
let foodItemPrice = document.querySelector("#new-item-price");


// On page load
document.addEventListener('DOMContentLoaded', () => {
    if(!adminToken) {
        errorDiv.lastChild.remove();
        showResponseMessage(section, `Please <a class="adm-login-link" href="login.html">login as admin here.</a>
        <br><br><a class="adm-login-link" href="menu.html">Homepage</a>`);
        logoutBtn.style.display = "None";
        document.querySelector("#orders-link").style.display = "None";
    }
    else {
        // Wait a while for all menu to load
        setTimeout(() => {
            addAdminBtns();
            for(let btn of pageBtns){
                addBtnCliclListeners(btn);
            }
        }, 1500);
    }
});

// Remove admin token on logout 
logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("adminToken");
});


function addToMenu() {
    let data = {
        "food_item_name": foodItemName.value,
        "food_item_price": +foodItemPrice.value
    };
    // POST menu item
    fetch(`${api_url}/menu`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${adminToken}`
        }
    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        message = responseJSON.message;
        if(message === "Food item added succesfully.") {
            // Reload menu page
            window.location.replace("adm_menu.html");
        }
        else {
            // Show message
            showResponseMessage(menuUL, message);
        }

        })
    .catch(function(error) {
        console.log(error);
    });
}

function updateMenuItem(foodId) {
    let data = {
        "food_item_name": foodItemName.value,
        "food_item_price": +foodItemPrice.value
    };
    // PUT menu item
    fetch(`${api_url}/menu/${foodId}`, {
        method: 'PUT',
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${adminToken}`
        }
    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        message = responseJSON.message;
        if(message === "Food item modified succesfully.") {
            // Reload menu page
            window.location.replace("adm_menu.html");
        }
        else {
            // Show message
            showResponseMessage(menuUL, message);
        }

        })
    .catch(function(error) {
        console.log(error);
    });
}

function deleteMenuItem(foodId) {
    // POST menu item
    fetch(`${api_url}/menu/${foodId}`, {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${adminToken}`
        }
    })
    .then((response) => response.json())
    .then(function(responseJSON) {
        message = responseJSON.message;
        showResponseMessage(section, message);
    })
    .catch(function(error) {
        console.log(error);
    });
}


function addAdminBtns() {
    // Select all menu item figcaptions
    let menuItemCaptions = document.querySelectorAll("figcaption");
    for(let item of menuItemCaptions) {
        // Appedn to each menu item a Modify and a Delete btn
        // Modify btn
        let modifyBtn = document.createElement("button");
        modifyBtn.classList.add("edit-btn");
        modifyBtn.innerHTML = "Modify";
        pageBtns.push(modifyBtn);                    // Extract foodId, foodName and foodPrice of item whose btn was clicked

        // Delete btn
        let deleteBtn = document.createElement("button");
        deleteBtn.classList.add("delete-btn");
        deleteBtn.innerHTML = "Delete";
        // Add event listener
        deleteBtn.addEventListener("click", (event) => {
            // Extract clickedItemid of item whose btn was clicked
            // Menu item
            let clickedMenuItem = event.target.parentNode.parentNode.parentNode;

            // id
            let clickedItemId = clickedMenuItem.querySelector("p.food-id").innerHTML.split("#")[1];
            // Call delete function
            deleteMenuItem(clickedItemId);
        });

        for(let btn of [modifyBtn, deleteBtn]) {
            btn.classList.add("admin-btn");
        }
        // Attach btns
        item.appendChild(modifyBtn);
        item.appendChild(deleteBtn);
    }
}

function addBtnCliclListeners(btn) {
    // Extract foodId, foodName and foodPrice of item whose btn was clicked
    let clickedMenuItem ;
    let clickedItemId;

    // On clicking add-new-btn, save btn, cancel btn or close btn

    // Add new btn
    if(btn.innerHTML === "Add Food Item") {
        btn.addEventListener("click", () => {
            // Display editing modal with no food item attributes
            document.querySelector("#new-item-name").value = "";
            document.querySelector("#new-item-price").value = "";
            
            // Hide update btn and show save btn
            updateBtn.style.display = "None";
            saveNewBtn.style.display = "inline-block";

            // Reveal editing modal on function call
            showEditModal();
        });
    }

    // Save btn
    else if(btn.value === "Save") {
        btn.addEventListener("click", () => {
            // Make POST request to server
            addToMenu();

            // Hide editing modal
            hideEditModal();
        });
    }

    // Close or Cancel btn
    else if(btn.innerHTML === "Close" || btn.value === "Cancel") {
        btn.addEventListener("click", () => {
            window.location.replace("adm_menu.html");
        });
    }

    // Modify btn
    else if(btn.innerHTML === "Modify") {
        btn.addEventListener("click", () => {
            showEditModal();

            // Extract foodId, foodName and foodPrice of item whose btn was clicked
            clickedMenuItem = btn.parentNode.parentNode.parentNode;
            // id
            window.clickedItemId = +clickedMenuItem.querySelector("p.food-id").innerHTML.split("#")[1];
            // Name
            let clickedItemName = clickedMenuItem.querySelector("p.item-name").innerHTML;
            // Price
            let clickedItemPrice = clickedMenuItem.querySelector("p.item-price").innerHTML;

            // Display editing modal with current food item attributes
            document.querySelector("#new-item-name").value = clickedItemName;
            document.querySelector("#new-item-price").value = +(clickedItemPrice.split(" ")[1]);

            // Show Update btn and hide Save btn
            saveNewBtn.style.display = "None";
            updateBtn.style.display = "inline-block";

        });
    }

    // Update btn
    else if(btn.value === "Update") {
        btn.addEventListener("click", () => {
            // Update item
            updateMenuItem(window.clickedItemId);
            
            hideEditModal();
        });
    }
}

function showEditModal() {
    for(let tag of [section, footer]) {
        tag.classList.add('hidden-mode');
    }
    editingForm.classList.remove("hidden-mode");
}

function hideEditModal() {
    for(let tag of [section, footer]) {
        tag.classList.remove('hidden-mode');
    }
    editingForm.classList.add("hidden-mode");
}
