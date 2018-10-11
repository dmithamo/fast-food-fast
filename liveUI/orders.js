// Consume API here
'use strict'; // Use ES6

const api_url = "https://dmithamo-fast-food-fast-api.herokuapp.com/api/v2";


// loginResp
let adminToken = localStorage.adminToken;
let loggedInSince = localStorage.loggedInSince;

// Helper function
const appendToparent = (element, parent) => {
    parent.appendChild(element);
};


// On document ready
document.addEventListener('DOMContentLoaded', () => {
    alert(adminToken);
    alert(loggedInSince);
});
