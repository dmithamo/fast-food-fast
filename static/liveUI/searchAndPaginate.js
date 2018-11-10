
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