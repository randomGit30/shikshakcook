const inputSide = document.getElementById('signup');
const emailSide = document.getElementById('signin');
const container = document.querySelector('.container');

inputSide.addEventListener('click', () => {
    container.classList.add('active');
});

emailSide.addEventListener('click', () => {
    container.classList.remove('active');
});
document.querySelectorAll('.overlay-left, .overlay-right').forEach(item => {
    item.addEventListener('mousemove', function(e) {
        const glow = this.querySelector('.glow');
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left; // X position within the element.
        const y = e.clientY - rect.top;  // Y position within the element.
        glow.style.left = `${x}px`;
        glow.style.top = `${y}px`;
    });
});
document.addEventListener('DOMContentLoaded', function() {
    // Function to move focus to next input on Enter key press
    function handleEnterKey(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the default form submit on Enter key
            var formElements = Array.from(event.target.form.elements);
            var currentIndex = formElements.indexOf(event.target);
            var nextIndex = currentIndex + 1;
            // Move focus to the next input field if it exists
            if (nextIndex < formElements.length) {
                formElements[nextIndex].focus();
            }
        }
    }

    // Attach the event listener to all input fields in both forms
    var form1Inputs = document.querySelectorAll('#form1 .query');
    var form2Inputs = document.querySelectorAll('#form2 .query');

    form1Inputs.forEach(input => input.addEventListener('keydown', handleEnterKey));
    form2Inputs.forEach(input => input.addEventListener('keydown', handleEnterKey));
});