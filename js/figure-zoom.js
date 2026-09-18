// Figure lightbox. Progressive enhancement: every image inside a post body
// becomes clickable; clicking opens it full-size over a dimmed overlay.
// Closes on overlay click, the close button, or Escape. Figures linked to
// vector or higher-resolution assets (SVG, 2x PNG) open at their native
// detail, which is what makes dense chart labels readable.
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var imgs = Array.prototype.slice.call(document.querySelectorAll('article.post img'));
    if (!imgs.length) return;

    var overlay = document.createElement('div');
    overlay.className = 'zoom-overlay';
    overlay.hidden = true;

    var frame = document.createElement('figure');
    frame.className = 'zoom-overlay__frame';

    var img = document.createElement('img');
    img.alt = '';

    var caption = document.createElement('figcaption');
    caption.className = 'zoom-overlay__caption';

    var close = document.createElement('button');
    close.className = 'zoom-overlay__close';
    close.type = 'button';
    close.setAttribute('aria-label', 'Close enlarged image');
    close.textContent = '\u00D7';

    frame.appendChild(img);
    frame.appendChild(caption);
    overlay.appendChild(frame);
    overlay.appendChild(close);
    document.body.appendChild(overlay);

    function open(src, alt, capText) {
      img.src = src;
      img.alt = alt || '';
      caption.textContent = capText || '';
      caption.hidden = !capText;
      overlay.hidden = false;
      document.body.style.overflow = 'hidden';
      close.focus();
    }

    function shut() {
      overlay.hidden = true;
      img.src = '';
      document.body.style.overflow = '';
    }

    imgs.forEach(function (el) {
      el.classList.add('img-zoomable');
      el.addEventListener('click', function () {
        var fig = el.closest('figure');
        var cap = fig ? fig.querySelector('figcaption') : null;
        open(el.currentSrc || el.src, el.alt, cap ? cap.textContent.trim() : '');
      });
    });

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay || e.target === frame) shut();
    });
    close.addEventListener('click', shut);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !overlay.hidden) shut();
    });
  });
})();
