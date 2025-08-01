// This file can be used for global JavaScript functions or initializations.
// Most specific AJAX logic is embedded directly in the relevant templates for simplicity.

// Example: Function to update cart count in the navbar (if not done by AJAX in view)
function updateCartCount(count) {
    const cartCountSpan = document.getElementById('cart-count');
    if (cartCountSpan) {
        cartCountSpan.innerText = count;
    }
}

// You might initialize some Bootstrap components here if needed, e.g., tooltips, popovers.
// var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
// var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
//   return new bootstrap.Tooltip(tooltipTriggerEl)
// })