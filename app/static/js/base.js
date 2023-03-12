document.addEventListener('DOMContentLoaded', () => {

  function Logout(event) {
      event.preventDefault();

      console.log('test1')

      fetch('/logout', {method: "POST"})
      .then(() => {
        window.location.href = '/';
        console.log('test2')
      });
    }


  elSignOutDesktop = document.getElementById('sign-out-desktop');
  console.log(elSignOutDesktop)
  if (elSignOutDesktop) {
     elSignOutDesktop.addEventListener('click', Logout);
  }

  elSignOutMobility = document.getElementById('sign-out-mobility');
  console.log(elSignOutMobility)
  if (elSignOutMobility) {
     elSignOutMobility.addEventListener('click', Logout)
  }

});
