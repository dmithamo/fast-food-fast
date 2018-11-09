// Consume API here
'use strict'; // Use ES6


// Append responseDiv to page
menuDiv.parentNode.insertBefore(responseDiv, menuDiv);
// Hide since it currently is empty
responseDiv.classList.add("hidden-mode");

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

// Collect new food item attributes
let foodItemName = document.querySelector("#new-item-name");
let foodItemPrice = document.querySelector("#new-item-price");
let foodItemImg = document.querySelector("#new-item-img");


// On page load
document.addEventListener('DOMContentLoaded', () => {
    if(!adminToken) {
        responseDiv.lastChild.remove();
        showResponseMessage(menuDiv, `Please <a class="adm-login-link" href="auth/login.html">login as admin here.</a>
        <br><br><a class="adm-login-link" href="/">Homepage</a>`);
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
    let foodName = capitalize(foodItemName.value);
    let data = {
        "food_item_name": foodName,
        "food_item_price": +foodItemPrice.value,
        "food_item_img": foodItemImg.value
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
    .then((response)=> {
        if(response.status < 500){
            return response.json()
        }
        else{
            location.replace('error_page')
        }
    })
    .then(function(responseJSON) {
        message = responseJSON.message;
        let food = responseJSON.food;
        if(message === "Food item added succesfully.") {
            // Hide editing div
            hideEditModal();
            // Show message
            showResponseMessage(menuDiv, `${message}<br><br><p class="order-summary">The food Item <br><br> foodItem ID: ${food.food_item_id}<br> foodItem name: ${food.food_item_name}<br>foodItem price: Ksh. ${food.food_item_price}<br> foodItem img: ${food.food_item_img}</p>`);
        }
        else {
            // Show message
            warningWrongValue.innerHTML = message;
            foodItemName.parentNode.insertBefore(warningWrongValue, foodItemName.nextSibling);
            highlightWrongInputOnForm(message);
        }

    })
    .catch(function(error) {
        console.log(error);
        window.location.replace("error_page");
    });
}

function updateMenuItem(foodId) {
    let foodName = capitalize(foodItemName.value);
    let data = {
        "food_item_name": foodName,
        "food_item_price": +foodItemPrice.value,
        "food_item_img": foodItemImg.value
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
    .then((response)=> {
        if(response.status < 500){
            return response.json()
        }
        else{
            location.replace('error_page')
        }
    })
    .then(function(responseJSON) {
        message = responseJSON.message;
        let food = responseJSON.food;
        if(message === "Food item modified succesfully.") {
            // Hide editing div
            hideEditModal();
            // Show message
            showResponseMessage(menuDiv, `${message}<br><br><p class="order-summary">The food Item <br><br> foodItem ID: ${food.food_item_id}<br> foodItem name: ${food.food_item_name}<br>foodItem price: Ksh. ${food.food_item_price}<br> foodItem img: ${food.food_item_img || "Generic image"}</p>`);

        }
        else {
            // Show message
            warningWrongValue.innerHTML = message;
            foodItemName.parentNode.insertBefore(warningWrongValue, foodItemName.nextSibling);
            highlightWrongInputOnForm(message);
        }

    })
    .catch(function(error) {
        console.log(error);
        window.location.replace("error_page");
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
    .then((response)=> {
        if(response.status < 500){
            return response.json()
        }
        else{
            location.replace('error_page')
        }
    })
    .then(function(responseJSON) {
        message = responseJSON.message;
        showResponseMessage(menuDiv, message);
    })
    .catch(function(error) {
        console.log(error);
        window.location.replace("error_page");
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
        pageBtns.push(modifyBtn);

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
            foodItemName.value = "";
            foodItemPrice.value = 0;
            
            // Hide update btn and show save btn
            updateBtn.style.display = "None";
            saveNewBtn.style.display = "inline-block";

            // Reveal editing modal on function call
            showEditModal();
            // Populate select with image options
            addImageOptions();
        });
    }

    // Save btn
    else if(btn.value === "Save") {
        btn.addEventListener("click", () => {
            checkParams(addToMenu, null);
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
            // Populate select with image options
            addImageOptions();

            // Extract foodId, foodName and foodPrice of item whose btn was clicked
            clickedMenuItem = btn.parentNode.parentNode.parentNode;
            // id
            window.clickedItemId = +clickedMenuItem.querySelector("p.food-id").innerHTML.split("#")[1];
            // Name
            let clickedItemName = clickedMenuItem.querySelector("p.item-name").innerHTML;
            // Price
            let clickedItemPrice = clickedMenuItem.querySelector("p.item-price").innerHTML;
            // Img
            let clickedItemImg = clickedMenuItem.querySelector("img").getAttribute("alt");

            let imagesSelect = document.querySelector("#new-item-img");
            // Set current img as the selected one
            for(let option of imagesSelect){
                if(option.value === clickedItemImg){
                    option.setAttribute("selected", "selected");
                }
            }

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
            // // Update item
            checkParams(updateMenuItem, window.clickedItemId);
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

function checkParams(funcToCall, arg) {
    if(!foodItemName.value){
        // If no name
        warningWrongValue.innerHTML = "Food item name cannot be blank!";
        foodItemName.parentNode.insertBefore(warningWrongValue, foodItemName.nextSibling);
        highlightWrongInputOnForm("Food item name");
    }

    // For invalid price
    if(+foodItemPrice.value < 1 ){
        // If no price
        warningWrongVal.innerHTML = "Food item price cannot be less than 1!";
        foodItemName.parentNode.insertBefore(warningWrongVal, foodItemPrice.nextSibling);
        highlightWrongInputOnForm("Food item price");
    }

    if(foodItemName.value && +foodItemPrice.value > 0 ){
        // Make POST / PUT request to server
        if(arg){
            funcToCall(arg);
        }
        else {
            funcToCall();
        }
    }
}

function capitalize(str) {
    // Capitalize fisrt letter
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

let searchBar = document.querySelector("#search-input")
searchBar.addEventListener('keyup', () => {
    searchFoodItem();
})

function searchFoodItem(){

    // Query for a meal with agiven name
    let foodFound = false;
    let searchTerm = searchBar.value.toLowerCase();
    // Remove whitespace
    searchTerm = searchTerm.replace(/(^\s+|\s+$)/g,'')
    // See if name of any of the items on menu matches searchTerm
    let allFoods = document.querySelectorAll(".item-name");
    
    let messagePara = document.querySelector("#search-empty");
    if(searchTerm !== ""){
        // If a valid searchTerm 
        for(let name of allFoods){
            let parentLi = name.parentNode.parentNode.parentNode;
            let foodItemName = name.innerHTML.toLowerCase();
            if(!foodItemName.includes(searchTerm)){
                parentLi.classList.add("hidden-mode");
            }
            if(foodItemName.includes(searchTerm)){
                parentLi.classList.remove("hidden-mode");
                foodFound = true;
            }
        }
    
        // Display message if no match
        let messagePara = document.querySelector("#search-empty");
        if(!foodFound) {
            messagePara.innerHTML = "Nothing found! :( Try tweaking the search term a bit";
        } else {
            messagePara.innerHTML = "";
            
        }
    }  else {
        // If a valid searchTerm 
        for(let name of allFoods){
            let parentLi = name.parentNode.parentNode.parentNode;
            parentLi.classList.remove("hidden-mode");
        }
        messagePara.innerHTML = "";

    }

}