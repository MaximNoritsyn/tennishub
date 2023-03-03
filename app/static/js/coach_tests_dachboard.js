document.addEventListener('DOMContentLoaded', function() {

    const searchInput = document.getElementById('search');
    const personSelect = document.getElementById('person');
    const addPersonButton = document.getElementById('add-person');
    const personsList = document.getElementById('persons-list');

    // Function to update the list of persons in the dropdown
    function updatePersonList(persons) {
    // Remove all existing options except for the first one
        while (personSelect.options.length > 1) {
            personSelect.remove(1);
        }

        // Add the new options to the select element
        for (let i = 0; i < persons.length; i++) {
            const option = document.createElement('option');
            option.value = persons[i].id_db;
            option.text = `${persons[i].name}`;
            personSelect.add(option);
        }

        // Enable the select element
        personSelect.disabled = false;
    }



    // Function to handle the search input
    function handleSearch() {
        const searchValue = searchInput.value.trim();

        // Only search if the search input has at least 3 characters
        if (searchValue.length >= 3) {
            fetch(`/api/persons?search=${searchValue}`)
                .then(response => response.json())
                .then(data => updatePersonList(data))
                .catch(error => console.error(error));
        }
    }

    // Add event listener to search input
    searchInput.addEventListener('input', handleSearch);


    const persons = [];

    addPersonButton.addEventListener('click', function(event) {
        event.preventDefault();
        const personOption = personSelect.options[personSelect.selectedIndex];
        const personId = personOption.value;
        const personName = personOption.text;

        const listItem = document.createElement('li');
        listItem.innerText = personName;
        personsList.appendChild(listItem);

        persons.push({id: personId, name: personName});

        personSelect.selectedIndex = 0;
    });


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
        event.preventDefault();
        const personsIds = persons.map(person => person.id);
        const personsInput = document.createElement('input');
        personsInput.type = 'hidden';
        personsInput.name = 'persons';
        personsInput.value = personsIds.join(',');;
        document.getElementById('form-coach-test').appendChild(personsInput);
        document.getElementById('form-coach-test').submit();
        }
    });
})
