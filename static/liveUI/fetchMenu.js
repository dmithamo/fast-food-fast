'use strict'; // Use ES6


// Select elements usable accross fucntions
// Menu
const menuUL = document.querySelector("#food-items");
const menuDiv = document.querySelector("#menu-div");

const foodImgs = {
    "Generic image": "https://15logo.net/wp-content/uploads/2017/05/fast-food-800x800.jpg",
    "Pizza": "http://www.a2zlifestyle.com/wp-content/uploads/2013/08/Healthy-and-Delicious-Pizza-at-Home.jpg",
    "Burger": "http://bk-latam-prod.s3.amazonaws.com/sites/burgerking.com.pe/files/MegaTocino_300x270px_0.png",
    "Fish": "https://img.aws.livestrongcdn.com/ls-article-image-673/cme/photography.prod.demandstudios.com/b676a889-db55-49ca-b1a1-3ced12ed8f10.jpg",
    "Soup": "https://skinnyms.com/wp-content/uploads/2012/09/Slow-Cooker-Hearty-Vegetable-and-Bean-Soup-1.jpg",
    "French fries": "http://theloadedslice.net/image/cache/products/appetizers/french-fries-800x800.png",
    "Bhajia": "http://vegindianrecipe.com/wp-content/uploads/2012/03/farali-bhajiya-large.jpg",
    "Sausage rolls": "http://richiemart.com/wp-content/uploads/2016/10/sausage-roll.jpg",
    "Milk shake": "https://www.americandairy.com/core/fileparse.php/111/urlt/vanilla-milkshake-recipe.jpg",
    "Coffee": "https://www.simplygreatcoffee.co.uk/shop/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/4/o/4oz_paper_cup_7.jpg",
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
                showMessageIfNoItems(menuUL, message);
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
                    liFoodId.innerHTML = `foodId#${foodItem.food_item_id}`;
                    
                    // Each li contains a figure
                    let liFigure = document.createElement("figure");

                    // Each figure contains an img
                    let img = document.createElement("img");
                    // Set img to a default img src for starters
                    img.src = foodImgs[`${foodItem.food_item_img}`];
                    img.alt = "Food Item";
                    
                    // Each figure contains a figcaption
                    let liFigCaption = document.createElement("figcaption");

                    // Each figcaption has a p tag to contain the name of the food_item
                    let liCapNameP = document.createElement("p");
                    liCapNameP.innerHTML = foodItem.food_item_name;
                    liCapNameP.classList.add("item-name");
                    
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
