// Define an array of IDs to select
const subAreaIds = ['area_power_1point', 'area_power_double'];

// Get all the elements with the specified IDs
const subActiveAreas = subAreaIds.map(id => document.getElementById(id));
const subPointInput = document.getElementById('sub_point');

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
      subSelectedElement.classList.remove('push-area');
      subPointInput.value = "";
    } else {
      subPointInput.value = element.id;
    }

    // Update the selected element variable to the clicked element
    subSelectedElement = element;
  });
});

// Fill the class 'push-area' to the active_area with the same id as the value of 'main_point' input
const subPointValue = subPointInput.value;
if (subPointValue) {
  const subActiveArea = document.getElementById(subPointValue);
  if (subActiveArea) {
    subActiveArea.classList.add('push-area');
    subSelectedElement = subActiveArea;
  }
}
