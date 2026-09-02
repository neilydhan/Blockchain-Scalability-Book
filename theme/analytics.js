/* Simple Analytics wiring for the Mastering Blockchain Scalability web edition.
 * Collects only the six aggregate events approved in ANALYTICS.md.
 * No metadata, no identifiers; honors Do Not Track. MIT-licensed build software.
 */
(function () {
  "use strict";

  var DNT =
    window.doNotTrack === "1" ||
    window.doNotTrack === 1 ||
    navigator.doNotTrack === "1" ||
    navigator.doNotTrack === "yes" ||
    navigator.msDoNotTrack === "1";

  function saReady() {
    return !DNT && window.sa_loaded === true && typeof window.sa_event === "function";
  }

  function fire(name) {
    if (saReady()) {
      try { window.sa_event(name); } catch (e) { /* never block reading */ }
    }
  }

  function fireAndGo(name, url) {
    var done = false;
    function go() {
      if (!done) {
        done = true;
        window.location.href = url;
      }
    }
    if (saReady()) {
      try {
        window.sa_event(name, go);
        setTimeout(go, 700);
      } catch (e) {
        go();
      }
    } else {
      go();
    }
  }

  function classify(link) {
    var href = (link.getAttribute("href") || "").toLowerCase();
    if (!href) return null;
    var text = (link.textContent || "").toLowerCase();
    if (/\.epub($|[?#])/.test(href) || (/releases\//.test(href) && /epub/.test(text))) return "download_epub";
    if (/\.pdf($|[?#])/.test(href) || /releases\//.test(href)) return "download_pdf";
    if (/citation\.cff($|[?#])/.test(href) || /zenodo|doi\.org/.test(href)) return "cite";
    if (/academic\.html($|[?#])/.test(href)) return "teach";
    if (/contributing\.html($|[?#])/.test(href)) return "contribute";
    if (/github\.com\/neilydhan\/blockchain-scalability-book\/(issues|pulls)/.test(href)) return "contribute";
    return null;
  }

  document.addEventListener("click", function (ev) {
    if (ev.defaultPrevented || ev.button !== 0 || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
    var link = ev.target && ev.target.closest ? ev.target.closest("a[href]") : null;
    if (!link) return;
    var name = classify(link);
    if (!name) return;
    if (link.target && link.target !== "_self") {
      fire(name); // new tab: best effort, never delay navigation
      return;
    }
    ev.preventDefault();
    fireAndGo(name, link.href);
  });

  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  onReady(function () {
    if (/\/chapters\/[^/]+\.html($|[?#])/.test(window.location.pathname) && !DNT && typeof window.sa_event === "function") {
      window.sa_event("chapter_view"); // placeholder queues it until latest.js loads
    }

    // Free-plan badge, required by the provider; the badge itself collects no data.
    if (!document.getElementById("sa-badge")) {
      var host = document.querySelector("main") || document.body;
      var wrap = document.createElement("div");
      wrap.id = "sa-badge";
      wrap.style.cssText = "margin:2.5rem 0 0.5rem;opacity:0.75;";
      wrap.innerHTML =
        '<a href="https://www.simpleanalytics.com/?utm_source=neilydhan.github.io&amp;utm_content=badge" referrerpolicy="origin" target="_blank" rel="noopener">' +
        '<picture>' +
        '<source srcset="https://simpleanalyticsbadges.com/neilydhan.github.io?mode=dark&amp;counter=false" media="(prefers-color-scheme: dark)">' +
        '<img src="https://simpleanalyticsbadges.com/neilydhan.github.io?mode=light&amp;counter=false" loading="lazy" referrerpolicy="no-referrer" crossorigin="anonymous" alt="Privacy-friendly analytics: Simple Analytics">' +
        "</picture></a>";
      host.appendChild(wrap);
    }
  });
})();
