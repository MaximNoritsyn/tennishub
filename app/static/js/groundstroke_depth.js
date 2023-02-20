// Define an array of IDs to select
const areaIds = ['box_1point_right', 'box_1point_left', 'box_2point', 'box_3point', 'box_4point'];

// Get all the elements with the specified IDs
const mainActiveAreas = areaIds.map(id => document.getElementById(id));

// Create a variable to keep track of the currently selected element
let mainSelectedElement = null;

// Add a click event listener to each active area element
mainActiveAreas.forEach((element) => {
  element.addEventListener('click', () => {
    // Remove the 'push-area' class from the currently selected element (if there is one)
    if (mainSelectedElement) {
      mainSelectedElement.classList.remove('push-area');
    }

    // Add the 'push-area' class to the clicked element
    element.classList.add('push-area');

    // If the clicked element is the same as the currently selected element, send a POST request to '/testing' with the element's ID as the data
    if (mainSelectedElement === element) {
      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/testing');
      xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
      xhr.send(JSON.stringify({ id: element.id }));
    }

    // Update the selected element variable to the clicked element
    mainSelectedElement = element;
  });
});


// Define an array of IDs to select
const subAreaIds = ['box_power_1point', 'box_power_double'];

// Get all the elements with the specified IDs
const subActiveAreas = subAreaIds.map(id => document.getElementById(id));

// Create a variable to keep track of the currently selected element
let subSelectedElement = null;

// Add a click event listener to each active area element
subActiveAreas.forEach((element) => {
  element.addEventListener('click', () => {
    // Remove the 'push-area' class from the currently selected element (if there is one)
    if (subSelectedElement) {
      subSelectedElement.classList.remove('push-area');
    }

    // Add the 'push-area' class to the clicked element
    element.classList.add('push-area');

    // If the clicked element is the same as the currently selected element, send a POST request to '/testing' with the element's ID as the data
    if (subSelectedElement === element) {
      selectedElement.classList.remove('push-area');
    }

    // Update the selected element variable to the clicked element
    subSelectedElement = element;
  });
});
