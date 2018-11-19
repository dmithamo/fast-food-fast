// Search
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

// Paginate
let itemsPerPage = 0;
let startAt = 0;

// Show different no. of items per page on admin and user pages
if(document.querySelector(".admin-portal-title").innerHTML  === "[ Admin Portal ]"){
    itemsPerPage = 4;
}
else {
    itemsPerPage = 3;
}


function paginate() {
    // Select all items
    let allMenuItems = document.querySelectorAll(".food-item");
    allMenuItems = Array.from(allMenuItems);

    let itemsToShow = allMenuItems.slice(startAt, itemsPerPage);
    // Original load
    displaySelectedItems(allMenuItems, itemsToShow);

    // When next is pressed 
    let nextBtn = document.querySelector(".next");
    nextBtn.addEventListener('click', () => {
        if(startAt+itemsPerPage < allMenuItems.length){
            startAt += itemsPerPage;
        }

        itemsToShow = allMenuItems.slice(startAt, startAt+itemsPerPage)
        displaySelectedItems(allMenuItems, itemsToShow)
    })
    

    // When prev is pressed 
    let prevBtn = document.querySelector(".previous");
    prevBtn.addEventListener('click', () => {
        if(startAt-itemsPerPage > 0){
            startAt -= itemsPerPage;
        }
        else {
            startAt = 0;
        }

        itemsToShow = allMenuItems.slice(startAt, startAt+itemsPerPage)
        displaySelectedItems(allMenuItems, itemsToShow)
    })
    
}

function displaySelectedItems(parentArray, subArray) {
    for(let item of parentArray){
        if(subArray.indexOf(item) < 0){
            item.classList.add("hidden-mode");
        }
        else {
            item.classList.remove("hidden-mode");
        }
    }
}
