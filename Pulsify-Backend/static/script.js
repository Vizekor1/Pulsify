document.addEventListener('DOMContentLoaded', function () {
    console.log('JavaScript loaded!');

    // Example: show an alert when a button is clicked
    const button = document.getElementById('myButton');
    if (button) {
        button.addEventListener('click', function () {
            alert('Button was clicked!');
        });
    }
});