document.addEventListener('DOMContentLoaded', () => {

  function Logout(event) {
      event.preventDefault();

      fetch('/logout', {method: "POST"})
      .then(() => {
        window.location.href = '/';
      });
    }


  elSignOutDesktop = document.getElementById('sign-out-desktop');
  if (elSignOutDesktop) {
     elSignOutDesktop.addEventListener('click', Logout);
  }

  elSignOutMobility = document.getElementById('sign-out-mobility');
  if (elSignOutMobility) {
     elSignOutMobility.addEventListener('click', Logout)
  }

});
