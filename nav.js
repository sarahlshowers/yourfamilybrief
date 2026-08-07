(function () {
  document.querySelectorAll('.nav-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var nav = btn.closest('nav');
      if (!nav) return;
      var open = nav.classList.toggle('nav-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  document.querySelectorAll('.nav-links .nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
      var nav = link.closest('nav');
      if (!nav) return;
      nav.classList.remove('nav-open');
      var btn = nav.querySelector('.nav-toggle');
      if (btn) btn.setAttribute('aria-expanded', 'false');
    });
  });

  document.addEventListener('click', function (e) {
    document.querySelectorAll('nav.nav-open').forEach(function (nav) {
      if (nav.contains(e.target)) return;
      nav.classList.remove('nav-open');
      var btn = nav.querySelector('.nav-toggle');
      if (btn) btn.setAttribute('aria-expanded', 'false');
    });
  });
})();
