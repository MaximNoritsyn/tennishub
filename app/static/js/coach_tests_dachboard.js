document.addEventListener('DOMContentLoaded', function() {

    const searchInput = document.getElementById('search');
    const personSelect = document.getElementById('person');
    const personsList = document.getElementById('persons-list');
    const personsList_Ch = document.getElementById('persons-list-for-choose');
    const searchDiv = document.getElementById('search-div');
    const editCoachTest = document.getElementById('edit-coach-test');
    const usernameEl = document.getElementById('username');
    let username = '';
    if (usernameEl) {
        username = usernameEl.value;
    }

    const groupTestIdEl = document.getElementById('group_test_id');
    let groupTestId = '';
    if (groupTestIdEl) {
        groupTestId = groupTestIdEl.value;
    }

    let persons = [];
    let players_ch = [];

    // Function to update the list of persons in the dropdown
    function updatePersonList(personsFromDb) {
        personsList_Ch.innerHTML = ''; // Clear the list

        personsFromDb = removePersonsFromPlayers(personsFromDb, persons)

        // Loop through the persons array and create new li elements for each person
        personsFromDb.forEach(person => {
          const li = document.createElement('li');
          li.textContent = person.name;
          li.setAttribute('id', person.id_db);

          li.addEventListener('click', function(event) {

                const listItem = document.createElement('li');
                listItem.innerText = person.name;
                personsList.appendChild(listItem);

                persons.push({id_db: person.id_db, name: person.name});
                li.remove();
            });

          personsList_Ch.appendChild(li);

        });
    }

    function removePersonsFromPlayers(players_ch, persons) {
      const idsToRemove = persons.map(person => person.id_db);
      return players_ch.filter(player => !idsToRemove.includes(player.id_db));
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

    handleSearch()

    if (groupTestId !== '') {
        fetch(`/api/coach_tests?group_test_id=${groupTestId}`)
                .then(response => response.json())
                .then(data => {

                    data.forEach(player => {
                        const listItem = document.createElement('li');
                        listItem.innerText = player.test_event.person.name;
                        personsList.appendChild(listItem);

                        persons.push({id_db: player.test_event.person.id_db, name: player.test_event.person.name});
                    })

                })
                .catch(error => console.error(error));
    }

    // Add a click event listener to the button
    editCoachTest.addEventListener('click', function(event) {
        event.preventDefault();

        if (editCoachTest.innerText === 'Редагувати') {

            searchDiv.style.display = 'block';  // show the div

            // Get the input elements by their IDs
            const assessorInput = document.getElementById('assessor');
            const dateInput = document.getElementById('v_date');
            const venueInput = document.getElementById('venue');

            // Remove the 'readonly' attribute from the input elements
            assessorInput.removeAttribute('readonly');
            dateInput.removeAttribute('readonly');
            venueInput.removeAttribute('readonly');

            // Change the submit button text
            editCoachTest.innerText = 'Зберегти';

        }
        else {

            const personsIds = persons.map(person => person.id_db);
            const personsInput = document.createElement('input');
            personsInput.type = 'hidden';
            personsInput.name = 'persons';
            personsInput.value = personsIds.join(',');;
            document.getElementById('form-coach-test').appendChild(personsInput);
            document.getElementById('form-coach-test').submit();

        }
    });
})
