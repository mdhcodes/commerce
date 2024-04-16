// Ensure the DOM has finished loading before the enclosed function(s) are executed.
document.addEventListener('DOMContentLoaded', function() {

    // NO - https://stackoverflow.com/questions/3008035/stop-an-input-field-in-a-form-from-being-submitted
    // Stop the input fields add to/remove from watchlist from being submitted when the button is clicked to place a bid. 

    const add = document.getElementById('#add');
    const remove = document.getElementById('#remove');
    const bid = document.getElementById('#bid');

    const placeBid = function() {
        bid.addEventListener('click', (e) => {
            e.preventDefault()

        })
    }










})