const activeAreas = document.querySelectorAll(".active-area");

activeAreas.forEach((element) => {
    element.classList.remove('active-area');
})

const elemValMobility = document.getElementById('test_event_mobility');
if (elemValMobility.value !== 0) {
    elemResMobility = document.getElementById(elemValMobility.value);
    elemResMobility.classList.add('marked-res');
}

const elemValItn = document.getElementById('test_event_itn');
if (elemValItn.value !== 0 ) {
    elemResItn = document.getElementById('itn_' + elemValItn.value);
    elemResItn.classList.add('marked-res');
}

