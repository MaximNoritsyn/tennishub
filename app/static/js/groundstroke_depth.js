const activeAreas = document.querySelectorAll(".active-area");
const elemGroundStroke1 = document.getElementById('groundstroke1');
const elemGroundStroke2 = document.getElementById('groundstroke2');

let selectedGroundStroke1 = null;
let selectedGroundStroke2 = null;

activeAreas.forEach((element) => {
  element.addEventListener('click', () => {
    if (selectedGroundStroke1 !== null && selectedGroundStroke2 !== null) {
      selectedGroundStroke1.classList.remove('groundstroke1');
      selectedGroundStroke2.classList.remove('groundstroke2');
      selectedGroundStroke1 = null;
      selectedGroundStroke2 = null;
      elemGroundStroke1.value = "";
      elemGroundStroke2.value = "";
    }

    if (selectedGroundStroke1 === null) {
        selectedGroundStroke1 = element
        element.classList.add('groundstroke1');
        elemGroundStroke1.value = element.id;
    } else {
        selectedGroundStroke2 = element
        element.classList.add('groundstroke2');
        elemGroundStroke2.value = element.id;
    }
  });
});


const valueGroundStroke1 = elemGroundStroke1.value;
if (valueGroundStroke1) {
  const activeGroundStroke1 = document.getElementById(valueGroundStroke1);
  if (activeGroundStroke1) {
    activeGroundStroke1.classList.add('groundstroke1');
    selectedGroundStroke1 = activeGroundStroke1;
  }
}

const valueGroundStroke2 = elemGroundStroke2.value;
if (valueGroundStroke2) {
  const activeGroundStroke1 = document.getElementById(valueGroundStroke2);
  if (activeGroundStroke2) {
    activeGroundStroke2.classList.add('groundstroke2');
    selectedGroundStroke2 = activeGroundStroke2;
  }
}
