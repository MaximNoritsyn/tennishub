const editCoachTest = document.getElementById('edit-coach-test');

// Add a click event listener to the button
editCoachTest.addEventListener('click', function(event) {
    // Prevent the default form submission
    if (editCoachTest.innerText === 'Редагувати') {
    event.preventDefault();

    // Get the input elements by their IDs
    const assessorInput = document.getElementById('assessor');
    const dateInput = document.getElementById('date');
    const venueInput = document.getElementById('venue');

    // Remove the 'readonly' attribute from the input elements
    assessorInput.removeAttribute('readonly');
    dateInput.removeAttribute('readonly');
    venueInput.removeAttribute('readonly');

    // Change the submit button text
    editCoachTest.innerText = 'Зберегти';
    }
    else {
    document.getElementById('form-coach-test').submit();
    }
});