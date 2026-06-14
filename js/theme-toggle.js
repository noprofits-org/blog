// Light/dark theme toggle for the masthead segmented control.
// The initial data-theme is set by an inline no-flash script in <head>.
(function () {
  function apply(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    var buttons = document.querySelectorAll('.theme-toggle button');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].classList.toggle('active', buttons[i].getAttribute('data-theme') === theme);
    }
  }

  function setTheme(theme) {
    try { localStorage.setItem('theme', theme); } catch (e) {}
    apply(theme);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var current = document.documentElement.getAttribute('data-theme') || 'light';
    apply(current);
    var buttons = document.querySelectorAll('.theme-toggle button');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener('click', function () {
        setTheme(this.getAttribute('data-theme'));
      });
    }
  });
})();
