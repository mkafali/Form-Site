document.addEventListener('DOMContentLoaded', function() {
  const darkModeToggle = document.getElementById('darkModeToggle');
  let darkModeEnabled = document.body.classList.contains('dark-mode');
    if(darkModeToggle){
  darkModeToggle.addEventListener('click', () => {
      darkModeEnabled = !darkModeEnabled;
      if (darkModeEnabled) {
          enableDarkMode();
      } else {
          disableDarkMode();
      }
      
  })};

  function enableDarkMode() {
      document.body.classList.add('dark-mode');
  }

  function disableDarkMode() {
      document.body.classList.remove('dark-mode');
  }
  
  

});
