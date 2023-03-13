document.addEventListener('DOMContentLoaded', function() {

    const searchInput = document.getElementById('search');
    const playersTableEl = document.getElementById('players-list');
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
            const testEventIdId = clickedElement.parentNode.id.split('_')[1];

            let url = `/coachtesting/${testEventIdId}/${currentTask.id}/1`;
            if (currentTask.id === 'serve') {
                url = `/coachtesting/${testEventIdId}/${currentTask.id}/1/1`;
            }
            else if (currentTask.id === 'mobility' || currentTask.id === 'results') {
                url = `/coachtesting/${testEventIdId}/${currentTask.id}`;
            }
            window.location.href = url;
        }
    }

    function addPlayer(event) {

        const clickedElement = event.target;
        const eventId = clickedElement.id.split('_')[1];

        const playerName = clickedElement.textContent;

        // Create a new row
        const newRow = document.createElement('tr');
        newRow.setAttribute('id', 'event_' + eventId);
        newRow.addEventListener('click', beginTaskTest)

        // Add cells to the row
        const nameCell = document.createElement('td');
        nameCell.textContent = playerName;
        newRow.appendChild(nameCell);

        const gsdCell = document.createElement('td');
        if (clickedElement.hasAttribute('finish_gsd')) {
            gsdCell.textContent = clickedElement.getAttribute('finish_gsd') === 'true' ? '✅' : '❌';
        }
        newRow.appendChild(gsdCell);

        const vdCell = document.createElement('td');
        if (clickedElement.hasAttribute('finish_vd')) {
            vdCell.textContent = clickedElement.getAttribute('finish_vd') === 'true' ? '✅' : '❌';
        }
        newRow.appendChild(vdCell);

        const gsaCell = document.createElement('td');
        if (clickedElement.hasAttribute('finish_gsa')) {
            gsaCell.textContent = clickedElement.getAttribute('finish_gsa') === 'true' ? '✅' : '❌';
        }
        newRow.appendChild(gsaCell);

        const serveCell = document.createElement('td');
        if (clickedElement.hasAttribute('finish_serve')) {
            serveCell.textContent = clickedElement.getAttribute('finish_serve') === 'true' ? '✅' : '❌';
        }
        newRow.appendChild(serveCell);

        const mobCell = document.createElement('td');
        if (clickedElement.hasAttribute('finish_mobility')) {
            mobCell.textContent = clickedElement.getAttribute('finish_mobility') === 'true' ? '✅' : '❌';
        }
        newRow.appendChild(mobCell);

        // Add the row to the tbody
        playersTableEl.appendChild(newRow);


        players.push(clickedElement.getAttribute('person_id'));
        clickedElement.remove();

    }


    // Function to update the list of persons in the dropdown
    function updatePersonList(personsFromDb) {
        personsListEl.innerHTML = ''; // Clear the list

        removePersonsFromPlayers(personsFromDb, players).forEach(person => {
          li = document.createElement('li');
          li.textContent = person.name;
          li.setAttribute('person_id', person.id_db);
          li.setAttribute('id', 'person_' + person.id_db);

          li.addEventListener('click', addPlayer);

          personsListEl.appendChild(li);

        });
    }




    function removePersonsFromPlayers(arrayToRemove, array) {
        console.log(array)
        console.log(arrayToRemove)
      return arrayToRemove.filter(l_person => !array.includes(l_person.id_db));
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
                        listItem.setAttribute('finish_gsd', coach_test.finish_gsd);
                        listItem.setAttribute('finish_vd', coach_test.finish_vd);
                        listItem.setAttribute('finish_gsa', coach_test.finish_gsa);
                        listItem.setAttribute('finish_serve', coach_test.finish_serve);
                        listItem.setAttribute('finish_mobility', coach_test.finish_mobility);
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

            const formCoachTest = document.getElementById('form-coach-test');
            if (formCoachTest) {
                formCoachTest.classList.add('edit-form');
            }

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
