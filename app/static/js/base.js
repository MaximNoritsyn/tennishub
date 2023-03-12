document.addEventListener('DOMContentLoaded', () => {

  function Logout(event) {
    event.preventDefault();

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/logout');

    xhr.noninterchangeable = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          console.log(xhr.responseText);
          location.reload();
          window.location.href = '/login';
        } else {
          console.error('Error:', xhr.status);
        }
      }
    };

    xhr.send();
  };

  elSignOutDesktop = document.getElementById('sign-out-desktop');
  if (elSignOutDesktop) {
     elSignOutDesktop.addEventListener('click', Logout);
  }

  elSignOutMobility = document.getElementById('sign-out-mobility');
  if (elSignOutMobility) {
     elSignOutMobility.addEventListener('click', Logout)
  }

});
