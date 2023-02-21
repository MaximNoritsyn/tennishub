// Define an array of IDs to select
const areaIds = ['area_1point_right', 'area_1point_left', 'area_2point', 'area_3point', 'area_4point'];

// Get all the elements with the specified IDs
const mainActiveAreas = areaIds.map(id => document.getElementById(id));
const mainPointInput = document.getElementById('main_point');

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
      mainSelectedElement.classList.remove('push-area');
      mainPointInput.value = "";
    } else {
      mainPointInput.value = element.id;
    }

    // Update the selected element variable to the clicked element
    mainSelectedElement = element;
  });
});


// Fill the class 'push-area' to the active_area with the same id as the value of 'main_point' input
const mainPointValue = mainPointInput.value;
if (mainPointValue) {
  const activeArea = document.getElementById(mainPointValue);
  if (activeArea) {
    activeArea.classList.add('push-area');
    mainSelectedElement = activeArea;
  }
}
