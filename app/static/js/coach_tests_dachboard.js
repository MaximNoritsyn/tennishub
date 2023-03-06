document.addEventListener('DOMContentLoaded', function() {

    const searchInput = document.getElementById('search');
    const personSelect = document.getElementById('person');
    const personsList = document.getElementById('persons-list');
    const personsList_Ch = document.getElementById('persons-list-for-choose');
    const searchDiv = document.getElementById('search-div');
    const usernameEl = document.getElementById('username');
    let username = '';
    if (usernameEl) {
        username = usernameEl.value;
    }

    // Function to update the list of persons in the dropdown
    function updatePersonList(persons) {
        personsList_Ch.innerHTML = ''; // Clear the list

        // Loop through the persons array and create new li elements for each person
        persons.forEach(person => {
          const li = document.createElement('li');
          li.textContent = person.name;
          li.setAttribute('id', person.id);

            li.addEventListener('click', function(event) {

                const listItem = document.createElement('li');
                listItem.innerText = person.name;
                personsList.appendChild(listItem);

                persons.push({id: person.id, name: person.name});
            });

          personsList_Ch.appendChild(li);

        });
    }



    // Function to handle the search input
    function handleSearch() {
        const searchValue = searchInput.value.trim();

        fetch(`/api/persons?search=${searchValue}&username=${username}`)
                .then(response => response.json())
                .then(data => updatePersonList(data))
                .catch(error => console.error(error));
    }

    // Add event listener to search input
    searchInput.addEventListener('input', handleSearch);


    const persons = [];
    const players_ch = [];

    handleSearch()

    const editCoachTest = document.getElementById('edit-coach-test');

    // Add a click event listener to the button
    editCoachTest.addEventListener('click', function(event) {
        // Prevent the default form submission
        if (editCoachTest.innerText === 'Редагувати') {
        event.preventDefault();

        searchDiv.style.display = 'block';  // show the div

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
