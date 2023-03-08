document.addEventListener('DOMContentLoaded', function() {

    const searchInput = document.getElementById('search');
    const playersListEl = document.getElementById('players-list');
    const personsListEl = document.getElementById('persons-list');
    const searchDiv = document.getElementById('search-div');
    const editCoachTest = document.getElementById('edit-coach-test');
    const usernameEl = document.getElementById('username');
    let username = '';
    if (usernameEl) {
        username = usernameEl.value;
    }

    const groupTestIdEl = document.getElementById('group-test-id');
    let groupTestId = '';
    if (groupTestIdEl) {
        groupTestId = groupTestIdEl.value;
    }

    let currentTask = null;
    let players = [];

    const taskBoxes = document.querySelectorAll('.task-box');
    taskBoxes.forEach((box) => {
        box.addEventListener('click', () => {
            if (currentTask !== null) {
                currentTask.classList.remove('current-task-box');
            }
            currentTask = box;
            currentTask.classList.add('current-task-box');
        });
    });

    function beginTaskTest(event) {
        if (currentTask) {

            const clickedElement = event.target;
            const testEventIdId = clickedElement.id.split('_')[1];

            const url = `/coachtesting/${testEventIdId}/${currentTask.id}/1`;
            window.location.href = url;
        }
    }

    function addPlayer(event) {

        const clickedElement = event.target;
        const eventId = clickedElement.id.split('_')[1];

        const playerName = clickedElement.textContent;

        const listItem = document.createElement('li');
        listItem.setAttribute('id', 'event_' + eventId);
        listItem.setAttribute('class', 'players-line');
        listItem.textContent = playerName;
        listItem.addEventListener('click', beginTaskTest)

        playersListEl.appendChild(listItem);

        players.push(clickedElement.person_id);
        clickedElement.remove();

    }


    // Function to update the list of persons in the dropdown
    function updatePersonList(personsFromDb) {
        personsListEl.innerHTML = ''; // Clear the list

        removePersonsFromPlayers(personsFromDb, players).forEach(person => {
          li = document.createElement('li');
          li.textContent = person.name;
          li.setAttribute('class', 'person-line');
          li.setAttribute('person_id', person.id_db);
          li.setAttribute('id', 'person_' + person.id_db);

          li.addEventListener('click', addPlayer);

          personsListEl.appendChild(li);

        });
    }




    function removePersonsFromPlayers(arrayToRemove, array) {
      return arrayToRemove.filter(l_person => !array.includes(l_person));
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

    if (groupTestId !== '') {
        fetch(`/api/coach_tests?group_test_id=${groupTestId}`)
                .then(response => response.json())
                .then(data => {

                    data.forEach(coach_test => {

                        const listItem = document.createElement('li');
                        listItem.setAttribute('id', 'saved-event_' + coach_test.test_event.id_db);
                        listItem.setAttribute('person_id', coach_test.test_event.person.id_db);
                        listItem.setAttribute('class', 'players-line');
                        listItem.textContent = coach_test.test_event.person.name;

                        addPlayer({target: listItem})

                    })

                })
                .catch(error => console.error(error));
    }

    handleSearch()

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

            const playersInput = document.createElement('input');
            playersInput.type = 'hidden';
            playersInput.name = 'players';
            playersInput.value = players.join(',');;
            document.getElementById('form-coach-test').appendChild(playersInput);
            document.getElementById('form-coach-test').submit();

        }
    });
})
