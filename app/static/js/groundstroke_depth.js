const activeAreas = document.querySelectorAll(".active-area");
const elemFirstBounce = document.getElementById('first_bounce');
const elemSecondBounce = document.getElementById('second_bounce');

let selectedFirstBounce = null;
let selectedSecondBounce = null;
let timeoutId;

activeAreas.forEach((element) => {
  element.addEventListener('click', () => {
    if (selectedFirstBounce !== null && selectedSecondBounce !== null) {
      selectedFirstBounce.classList.remove('first_bounce');
      selectedSecondBounce.classList.remove('second_bounce');
      selectedFirstBounce = null;
      selectedSecondBounce = null;
      elemFirstBounce.value = "";
      elemSecondBounce.value = "";
      clearTimeout(timeoutId);
    }

    if (selectedFirstBounce === null) {
        selectedFirstBounce = element
        element.classList.add('first_bounce');
        elemFirstBounce.value = element.id;
    } else {
        selectedSecondBounce = element
        element.classList.add('second_bounce');
        elemSecondBounce.value = element.id;
        timeoutId = setTimeout(submitForm, 1000);
    }
  });
});


const valueFirstBounce = elemFirstBounce.value;
if (valueFirstBounce) {
  const activeFirstBounce = document.getElementById(valueFirstBounce);
  if (activeFirstBounce) {
    activeFirstBounce.classList.add('first_bounce');
    selectedFirstBounce = activeFirstBounce;
  }
}

const valueSecondBounce = elemSecondBounce.value;
if (valueSecondBounce) {
  const activeSecondBounce = document.getElementById(valueSecondBounce);
  if (activeSecondBounce) {
    activeSecondBounce.classList.add('second_bounce');
    selectedSecondBounce = activeSecondBounce;
  }
}

function submitForm() {
  document.getElementById('result_serving_ball').submit();
}
