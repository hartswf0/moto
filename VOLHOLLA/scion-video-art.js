/* SCION video art: when a track that has a music video plays, the artwork slot shows the film,
   muted and locked to the audio clock (the audio element stays the single source of truth).
   Self-contained: it learns which <audio> is playing by observing HTMLMediaElement.play, so the
   song and album players need no changes beyond loading this file. */
(function () {
  "use strict";
  // keyed by the audio file's basename (decoded); values are paths relative to /VOLHOLLA/
  var VIDEOS = {
    "Et tu, Brute_ - Wittgenstein's Backpack - Treblo.ogg": { src: "../scion/wittgensteins-backpack/wittgensteins-backpack.mp4", page: "../scion/wittgensteins-backpack/index.html", swarm: "SCION 01 Gilliam · 08 Sutherland" },
    "Et tu, Brute_ - Corrugated Sky - Treblo.ogg": { src: "../scion/corrugated-sky/corrugated-sky.mp4", page: "../scion/corrugated-sky/index.html", swarm: "SCION 02 Reiniger" },
    "Et tu, Brute_ - The Whole Package - Treblo.ogg": { src: "../scion/the-whole-package/the-whole-package.mp4", page: "../scion/the-whole-package/index.html", swarm: "SCION 05 Norstein" },
    "Et tu, Brute_ - The Universal Boxback - Treblo.ogg": { src: "../scion/the-universal-boxback/the-universal-boxback.mp4", page: "../scion/the-universal-boxback/index.html", swarm: "SCION 06 Whitney" }
  };
  var SLOT_SELECTORS = ["#artSquare", ".art-square", ".cover-square"];
  var DRIFT = 0.25; // seconds of allowed picture/sound drift before a hard re-seek

  var current = null, video = null, badge = null, slot = null, entry = null, raf = 0;

  function basename(url) {
    try { return decodeURIComponent(String(url || "").split("?")[0].split("#")[0].split("/").pop()); } catch (e) { return ""; }
  }
  function findSlot() {
    for (var i = 0; i < SLOT_SELECTORS.length; i++) { var el = document.querySelector(SLOT_SELECTORS[i]); if (el) return el; }
    return null;
  }
  function ensureStyle() {
    if (document.getElementById("scion-video-art-style")) return;
    var css = ".scion-video-art{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#000;z-index:2;opacity:0;transition:opacity .35s ease}" +
      ".scion-video-art.is-on{opacity:1}" +
      ".scion-video-badge{position:absolute;left:8px;bottom:8px;z-index:3;font:700 11px/1 ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;" +
      "background:rgba(0,0,0,.72);color:#f2382c;padding:6px 8px;border-radius:4px;text-decoration:none;opacity:0;transition:opacity .35s ease}" +
      ".scion-video-badge.is-on{opacity:1}";
    var s = document.createElement("style"); s.id = "scion-video-art-style"; s.textContent = css; document.head.appendChild(s);
  }
  function teardown() {
    if (video) { video.classList.remove("is-on"); video.pause(); }
    if (badge) badge.classList.remove("is-on");
    entry = null;
  }
  function attach(audio) {
    var e = VIDEOS[basename(audio.currentSrc || audio.src)];
    if (!e) { teardown(); return; }
    slot = findSlot(); if (!slot) return;
    ensureStyle();
    if (getComputedStyle(slot).position === "static") slot.style.position = "relative";
    if (!video || video.parentNode !== slot) {
      video = document.createElement("video");
      video.className = "scion-video-art"; video.muted = true; video.defaultMuted = true;
      video.playsInline = true; video.setAttribute("playsinline", ""); video.setAttribute("muted", "");
      video.preload = "auto"; video.setAttribute("aria-label", "Music video, synced to the song");
      video.addEventListener("loadeddata", function () { sync(true); });
      // a missing or undecodable film must never hide the artwork
      video.addEventListener("error", function () { teardown(); entry = null; });
      slot.appendChild(video);
      badge = document.createElement("a"); badge.className = "scion-video-badge"; badge.target = "_self";
      slot.appendChild(badge);
    }
    if (entry !== e) {
      entry = e; video.src = e.src; badge.href = e.page; badge.textContent = "▶ video · " + e.swarm;
    }
    var show = function () { if (entry === e) { video.classList.add("is-on"); badge.classList.add("is-on"); } };
    if (video.readyState >= 2) show(); else video.addEventListener("loadeddata", show, { once: true });
    sync(true);
  }
  function sync(force) {
    if (!video || !current || !entry) return;
    var t = current.currentTime || 0;
    if (video.readyState >= 1) {
      if (force || Math.abs(video.currentTime - t) > DRIFT) { try { video.currentTime = Math.min(t, (video.duration || t) - 0.05); } catch (e) {} }
      if (video.playbackRate !== current.playbackRate) video.playbackRate = current.playbackRate || 1;
    }
    if (current.paused) { if (!video.paused) video.pause(); }
    else if (video.paused) { var p = video.play(); if (p && p.catch) p.catch(function () {}); }
  }
  function loop() { sync(false); raf = (current && !current.paused) ? requestAnimationFrame(loop) : 0; }
  function watch(audio) {
    if (current === audio) { attach(audio); return; }
    current = audio;
    ["play", "playing", "pause", "seeked", "ratechange", "ended"].forEach(function (ev) {
      audio.addEventListener(ev, function () { if (audio !== current) return; sync(ev === "seeked"); if (!raf && !audio.paused) raf = requestAnimationFrame(loop); });
    });
    ["loadstart", "loadedmetadata", "emptied"].forEach(function (ev) {
      audio.addEventListener(ev, function () { if (audio === current) attach(audio); });
    });
    attach(audio);
  }
  var origPlay = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function () {
    var r = origPlay.apply(this, arguments);
    if (this instanceof HTMLAudioElement || (this.tagName === "AUDIO")) { try { watch(this); } catch (e) {} if (!raf) raf = requestAnimationFrame(loop); }
    return r;
  };
  window.SCION_VIDEO_ART = { videos: VIDEOS };
})();
