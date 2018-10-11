// Consume API here
'use strict'; // Use ES6

const api_url = "https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2";

// Select elements usable accross fucntions
// Menu
const menuUL = document.querySelector("#food-items");
const menuContainer = document.querySelector("#menu-cont");

// Helper function
const appendToparent = (element, parent) => {
    parent.appendChild(element);
};


function fetchMenu() {
    // fetch menu
    fetch(`${api_url}/menu`)
        // Convert response object to json object 
        .then((response)=> response.json())
        // Query json object for specific items
        .then(function(responseJSON) {
            let message = responseJSON.message;
            if(message === "No food items on the menu yet") {
                // Create and style a special paragraph to report that menu is empty
                let specialPara = document.createElement("p");
                specialPara.innerHTML = message;
                specialPara.classList.add("msg-paragraph");

                // Append to page
                menuUL.parentNode.insertBefore(specialPara, menuUL);
            }
            else {
                // Create an li for each item on menu and append li to menuUL
                let menuItems = responseJSON.menu;
                menuItems.forEach(foodItem => {
                    // Create the elements that make up each food_item li on the menu

                    // Each item as an li
                    let foodLi = document.createElement("li");
                    // Style li by adding class
                    foodLi.classList.add("food-item");

                    // Each li has a p tag for the food_item_id
                    let liFoodId = document.createElement("p");
                    liFoodId.classList.add("food-id");
                    liFoodId.innerHTML = foodItem.food_item_id;
                    
                    // Each li contains a figure
                    let liFigure = document.createElement("figure");

                    // Each figure contains an img
                    let img = document.createElement("img");
                    // Set img to a default img src for starters
                    img.src = "https://15logo.net/wp-content/uploads/2017/05/fast-food-800x800.jpg";
                    img.alt = "Food Item";
                    
                    // Each figure contains a figcaption
                    let liFigCaption = document.createElement("figcaption");

                    // Each figcaption has a p tag to contain the name of the food_item
                    let liCapNameP = document.createElement("p");
                    liCapNameP.innerHTML = foodItem.food_item_name;
                    
                    // Each figcaption has a p tag to contain the price of the food_item
                    let liCapPriceP = document.createElement("p");
                    liCapPriceP.innerHTML = `Ksh. ${foodItem.food_item_price}`;
                    // Style price by adding className
                    liCapPriceP.classList.add("item-price");

                    // Append elements to make up the food_item
                    appendToparent(img, liFigure);

                    [liCapNameP, liCapPriceP].forEach(p => {
                        appendToparent(p, liFigCaption);
                    });

                    appendToparent(liFigCaption, liFigure);
                    
                    for(let tag of [liFoodId, liFigure]) {
                        appendToparent(tag, foodLi);
                    }

                    // Append li to list of food items (the menu)
                    appendToparent(foodLi, menuUL);
                });
            }
        })
        .catch(function(err) {
            console.log(err);
        });
}


// Call function when DOM content is finished loading
document.addEventListener('DOMContentLoaded', () => {
    fetchMenu();
});
