// Home-page featured-post randomizer. Progressive enhancement: the server bakes
// the newest post that HAS A FIGURE into the featured slot (so the card is valid
// with JS off and for crawlers). On each visit this swaps in a random
// figure-having post, fetching only that one post's figure — so the home page
// stays light instead of shipping every post's diagram. Any failure leaves the
// baked default untouched.
//
// Eligible posts are the "Latest" rows tagged data-has-figure (Blog.Context's
// hasFigure marker). The text column is read from that row; the figure is pulled
// from the post's own page and its URLs absolutized so they resolve from "/".
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var featured = document.querySelector('.featured');
    if (!featured) return;
    var grid = featured.querySelector('.featured-grid');
    var dateEl = featured.querySelector('.featured-date');
    if (!grid) return;

    var rows = Array.prototype.slice.call(
      document.querySelectorAll('.post-row[data-has-figure]'));
    if (!rows.length) return;

    var curLink = featured.querySelector('.featured-title a');
    var curUrl = curLink ? curLink.getAttribute('href') : null;

    function pathOf(u) {
      try { return new URL(u, location.href).pathname; } catch (e) { return u || ''; }
    }

    // Hide whichever Latest row is the currently-featured post, so it isn't
    // duplicated above. A class (not the [hidden] attribute) so the topic filter,
    // which drives [hidden], can't un-hide it.
    function reconcile(url) {
      var p = pathOf(url);
      Array.prototype.slice.call(document.querySelectorAll('.post-row'))
        .forEach(function (r) {
          r.classList.toggle('is-featured', pathOf(r.getAttribute('href')) === p);
        });
    }

    // Random eligible row, avoiding the immediately-previous pick and the baked
    // default so the card visibly changes on a new visit.
    var LAST = 'np-featured-last', last = null;
    try { last = sessionStorage.getItem(LAST); } catch (e) {}
    var choices = rows.filter(function (r) {
      var p = pathOf(r.getAttribute('href'));
      return p !== pathOf(last) && p !== pathOf(curUrl);
    });
    if (!choices.length) {
      choices = rows.filter(function (r) {
        return pathOf(r.getAttribute('href')) !== pathOf(curUrl);
      });
    }
    if (!choices.length) { reconcile(curUrl); return; }

    var pick = choices[Math.floor(Math.random() * choices.length)];
    var url = pick.getAttribute('href');
    try { sessionStorage.setItem(LAST, url); } catch (e) {}
    var base = new URL(url, location.href);

    function esc(s) { var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
    function text(sel) { var n = pick.querySelector(sel); return n ? n.textContent.trim() : ''; }

    fetch(url).then(function (r) {
      if (!r.ok) throw new Error('fetch ' + r.status);
      return r.text();
    }).then(function (html) {
      var doc = new DOMParser().parseFromString(html, 'text/html');
      var fig = doc.querySelector('.tikz-figure, .post-body figure');
      if (!fig) throw new Error('no figure');

      // Caption: an <img> figure carries its own <figcaption>; a TikZ div is
      // followed by a "Figure N." paragraph (same pairing the server uses).
      var capHtml = '', innerCap = fig.querySelector('figcaption');
      if (innerCap) { capHtml = innerCap.innerHTML; innerCap.remove(); }
      else {
        var sib = fig.nextElementSibling;
        if (sib && sib.tagName === 'P' && /^\s*(<(strong|em)>)?\s*Figure\b/i.test(sib.innerHTML)) {
          capHtml = sib.innerHTML;
        }
      }
      // The featured card has its own "Fig. 1" label, so drop a leading
      // "Figure N." marker from the borrowed caption.
      capHtml = capHtml.replace(/^\s*<(strong|em)>\s*Figure\s+\d+\.?\s*<\/\1>\s*/i, '')
                       .replace(/^\s*Figure\s+\d+\.?\s*/i, '');

      // Absolutize asset/link URLs so they resolve from "/".
      Array.prototype.slice.call(fig.querySelectorAll('img[src], a[href]'))
        .forEach(function (el) {
          var attr = el.hasAttribute('src') ? 'src' : 'href';
          try { el.setAttribute(attr, new URL(el.getAttribute(attr), base).href); } catch (e) {}
        });
      var figMarkup = fig.classList.contains('tikz-figure') ? fig.outerHTML : fig.innerHTML;

      var title = text('.post-row-title'), desc = text('.post-row-desc'),
          topic = text('.post-row-topic'), date = text('.post-row-date');
      var tags = Array.prototype.slice.call(pick.querySelectorAll('.post-row-tags .row-tag'))
        .map(function (t) { return t.textContent.replace(/^#/, '').trim(); }).filter(Boolean);

      if (dateEl && date) dateEl.textContent = date;

      grid.innerHTML =
        '<div class="featured-text">' +
          (topic ? '<span class="featured-topic">' + esc(topic) + '</span>' : '') +
          '<h2 class="featured-title"><a href="' + esc(url) + '">' + esc(title) + '</a></h2>' +
          (desc ? '<p class="featured-desc">' + esc(desc) + '</p>' : '') +
          (tags.length ? '<div class="tag-chips">' + tags.map(function (t) {
            return '<span class="tag-chip">' + esc(t) + '</span>'; }).join('') + '</div>' : '') +
          '<a class="featured-readmore" href="' + esc(url) + '">Read the note →</a>' +
        '</div>' +
        '<figure class="featured-figure">' +
          '<div class="figure-label">Fig. 1</div>' +
          '<div class="figure-body">' + figMarkup + '</div>' +
          (capHtml ? '<figcaption class="figure-caption">' + capHtml + '</figcaption>' : '') +
        '</figure>';

      reconcile(url);
    }).catch(function () { reconcile(curUrl); });
  });
})();
