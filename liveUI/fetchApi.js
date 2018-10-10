// Consume API here
'use strict'; // Use ES6

const api_url = "https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2";

// fetch menu
fetch(`${api_url}/menu`, {
    mode: "same-origin",
})
    .then(function(response) {
        console.log(response);

    })
    .catch(function(err) {
        console.log(err);
    })