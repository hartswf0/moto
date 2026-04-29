(function () {
  const els = {
    deck: document.querySelector(".radio-deck"),
    dial: document.getElementById("radioDial"),
    dialMark: document.getElementById("dialMark"),
    dialTitle: document.getElementById("dialTitle"),
    state: document.getElementById("radioState"),
    count: document.getElementById("radioCount"),
    title: document.getElementById("trackTitle"),
    album: document.getElementById("albumTitle"),
    art: document.getElementById("trackArt"),
    artFallback: document.getElementById("artFallback"),
    prev: document.getElementById("prevBtn"),
    play: document.getElementById("playBtn"),
    next: document.getElementById("nextBtn"),
    shuffle: document.getElementById("shuffleBtn"),
    auto: document.getElementById("autoBtn"),
    songLink: document.getElementById("songPageLink"),
    seek: document.getElementById("seekBar"),
    timeNow: document.getElementById("timeNow"),
    timeTotal: document.getElementById("timeTotal"),
    queue: document.getElementById("queueList"),
    reshuffle: document.getElementById("reshuffleBtn")
  };

  const audio = new Audio();
  audio.preload = "metadata";
  let catalog = [];
  let order = [];
  let position = 0;
  let shuffleMode = true;
  let autoMode = true;
  let seeking = false;

  function fmtTime(sec) {
    if (!Number.isFinite(sec) || sec < 0) return "0:00";
    const m = Math.floor(sec / 60);
    const r = Math.floor(sec % 60);
    return `${m}:${String(r).padStart(2, "0")}`;
  }

  function pathFromRoot(source) {
    if (!source) return "";
    if (/^https?:\/\//i.test(source)) return source;
    if (source.startsWith("VOLHOLLA/")) return `./${source.slice("VOLHOLLA/".length)}`;
    return `../${source}`;
  }

  function songHref(source) {
    if (!source) return "./index.html";
    if (/^https?:\/\//i.test(source)) return source;
    if (source.startsWith("VOLHOLLA/")) return `./${source.slice("VOLHOLLA/".length)}`;
    return `../${source}`;
  }

  function pickArt(album, track) {
    return track?.art?.source || album?.defaultTrackArt?.source || album?.cover?.source || "";
  }

  function pickAudio(track) {
    return track?.audio?.source || track?.source || "";
  }

  function shuffleArray(items) {
    const next = items.slice();
    for (let i = next.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [next[i], next[j]] = [next[j], next[i]];
    }
    return next;
  }

  function buildOrder(keepCurrent = true) {
    const current = catalog[order[position]];
    order = shuffleMode
      ? shuffleArray(catalog.map((_, index) => index))
      : catalog.map((_, index) => index);
    if (keepCurrent && current) {
      const idx = order.findIndex((item) => catalog[item] === current);
      if (idx > 0) {
        order.splice(idx, 1);
        order.unshift(catalog.indexOf(current));
      }
    }
    position = 0;
  }

  function currentTrack() {
    return catalog[order[position]] || null;
  }

  function setAccent(track) {
    const a = track?.accentA || "#7df2c8";
    const b = track?.accentB || "#f4c95d";
    document.documentElement.style.setProperty("--accent-a", a);
    document.documentElement.style.setProperty("--accent-b", b);
  }

  function renderQueue() {
    if (!els.queue) return;
    const rows = order.slice(position, position + 10).map((catalogIndex, offset) => {
      const track = catalog[catalogIndex];
      return `
        <li class="${offset === 0 ? "is-current" : ""}">
          <span>${String(position + offset + 1).padStart(2, "0")}</span>
          <span class="name">${escapeHtml(track.title)} <span class="album">/ ${escapeHtml(track.albumLabel)}</span></span>
        </li>
      `;
    }).join("");
    els.queue.innerHTML = rows || "<li><span>--</span><span class=\"name\">No tracks loaded</span></li>";
  }

  function escapeHtml(value) {
    return String(value || "").replace(/[&<>"']/g, (ch) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "\"": "&quot;",
      "'": "&#39;"
    }[ch]));
  }

  function updateUI() {
    const track = currentTrack();
    const playing = !audio.paused && !!audio.src;
    document.body.classList.toggle("is-live", playing);
    els.dial?.classList.toggle("is-playing", playing);
    els.shuffle?.classList.toggle("is-on", shuffleMode);
    els.shuffle?.setAttribute("aria-pressed", shuffleMode ? "true" : "false");
    els.auto?.classList.toggle("is-on", autoMode);
    els.auto?.setAttribute("aria-pressed", autoMode ? "true" : "false");

    if (!track) {
      if (els.state) els.state.textContent = "Empty";
      if (els.count) els.count.textContent = "0 tracks";
      return;
    }

    setAccent(track);
    if (els.state) els.state.textContent = playing ? "Broadcasting" : audio.src ? "Paused" : "Ready";
    if (els.count) els.count.textContent = `${catalog.length} tracks / ${position + 1}`;
    if (els.title) els.title.textContent = track.title;
    if (els.album) els.album.textContent = track.albumLabel;
    if (els.dialMark) els.dialMark.textContent = playing ? "ON AIR" : "TUNED";
    if (els.dialTitle) els.dialTitle.textContent = shuffleMode ? "SHUF" : "SEQ";
    if (els.play) els.play.textContent = playing ? "Pause" : audio.src ? "Resume" : "Start Radio";
    if (els.songLink) els.songLink.href = songHref(track.songPage);

    const pct = Number.isFinite(audio.duration) && audio.duration > 0
      ? Math.max(0, Math.min(1000, Math.round((audio.currentTime / audio.duration) * 1000)))
      : 0;
    if (!seeking && els.seek) els.seek.value = String(pct);
    if (els.timeNow) els.timeNow.textContent = fmtTime(audio.currentTime);
    if (els.timeTotal) els.timeTotal.textContent = fmtTime(audio.duration);

    const art = pathFromRoot(track.art);
    if (els.art && art) {
      els.art.src = encodeURI(art);
      els.art.alt = `${track.title} artwork`;
      els.art.hidden = false;
      if (els.artFallback) els.artFallback.hidden = true;
    } else if (els.art) {
      els.art.hidden = true;
      if (els.artFallback) els.artFallback.hidden = false;
    }
    renderQueue();
  }

  function load(positionIndex, autoplay = false) {
    if (!catalog.length) return;
    position = Math.max(0, Math.min(order.length - 1, positionIndex));
    const track = currentTrack();
    audio.src = encodeURI(pathFromRoot(track.audio));
    audio.load();
    updateUI();
    if (autoplay) {
      audio.play().catch(() => updateUI());
    }
  }

  function playPause() {
    if (!catalog.length) return;
    if (!audio.src) {
      load(position, true);
      return;
    }
    if (audio.paused) audio.play().catch(() => updateUI());
    else audio.pause();
  }

  function next(autoplay = false) {
    if (!catalog.length) return;
    if (position >= order.length - 1) buildOrder(false);
    else position += 1;
    load(position, autoplay);
  }

  function prev() {
    if (!catalog.length) return;
    if (audio.currentTime > 3) {
      audio.currentTime = 0;
      updateUI();
      return;
    }
    position = position > 0 ? position - 1 : order.length - 1;
    load(position, true);
  }

  async function loadCatalog() {
    const response = await fetch("./media-manifest.json", { cache: "no-cache" });
    const manifest = await response.json();
    const albums = manifest.albums || {};
    catalog = Object.values(albums).flatMap((album) => {
      const tracks = Array.isArray(album.tracks) ? album.tracks : [];
      return tracks.map((track) => ({
        title: track.title,
        albumLabel: album.label || album.key,
        audio: pickAudio(track),
        art: pickArt(album, track),
        songPage: track.songPage,
        accentA: album.accentA,
        accentB: album.accentB
      })).filter((track) => track.audio);
    });
    buildOrder(false);
    if (els.count) els.count.textContent = `${catalog.length} tracks`;
    updateUI();
  }

  els.dial?.addEventListener("click", playPause);
  els.play?.addEventListener("click", playPause);
  els.next?.addEventListener("click", () => next(true));
  els.prev?.addEventListener("click", prev);
  els.shuffle?.addEventListener("click", () => {
    shuffleMode = !shuffleMode;
    buildOrder(true);
    updateUI();
  });
  els.auto?.addEventListener("click", () => {
    autoMode = !autoMode;
    updateUI();
  });
  els.reshuffle?.addEventListener("click", () => {
    shuffleMode = true;
    buildOrder(true);
    updateUI();
  });
  els.seek?.addEventListener("pointerdown", () => { seeking = true; });
  els.seek?.addEventListener("pointerup", () => { seeking = false; });
  els.seek?.addEventListener("input", () => {
    if (!Number.isFinite(audio.duration) || audio.duration <= 0) return;
    const target = (Number(els.seek.value) / 1000) * audio.duration;
    if (els.timeNow) els.timeNow.textContent = fmtTime(target);
  });
  els.seek?.addEventListener("change", () => {
    if (Number.isFinite(audio.duration) && audio.duration > 0) {
      audio.currentTime = (Number(els.seek.value) / 1000) * audio.duration;
    }
    seeking = false;
  });

  audio.addEventListener("play", updateUI);
  audio.addEventListener("pause", updateUI);
  audio.addEventListener("timeupdate", updateUI);
  audio.addEventListener("loadedmetadata", updateUI);
  audio.addEventListener("ended", () => {
    if (autoMode) next(true);
    else updateUI();
  });
  audio.addEventListener("error", () => {
    if (els.state) els.state.textContent = "Signal lost";
    if (autoMode) window.setTimeout(() => next(true), 650);
  });

  loadCatalog().catch((error) => {
    console.warn("Radio catalog failed", error);
    if (els.state) els.state.textContent = "Catalog error";
    if (els.count) els.count.textContent = "Manifest unavailable";
  });
})();
