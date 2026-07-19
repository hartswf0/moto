(() => {
  "use strict";

  const mix = window.WC_2026_FINAL_MIX;
  if (!mix?.tracks?.length) return;

  const STORAGE_KEY = "wc2026-listening-desk-v2";
  const rawTracks = mix.tracks.map((track) => ({ ...track, id: track.songPage }));
  const trackById = new Map(rawTracks.map((track) => [track.id, track]));
  const analysis = window.WC_2026_AUDIO_ANALYSIS || { tracks: [], suggestedOrder: [] };
  const analysisById = new Map((analysis.tracks || []).map((record) => [record.id, record]));
  const canonicalOrder = rawTracks.map((track) => track.id);
  const sortLabels = {
    custom: "CUSTOM ORDER",
    drama: "DRAMA ARC",
    "pace-up": "PACE LOW TO HIGH",
    "pace-down": "PACE HIGH TO LOW",
    energy: "ENERGY HIGH TO LOW",
    bpm: "BPM LOW TO HIGH",
    lyrics: "LYRICS FIRST",
    instrumental: "INSTRUMENTAL FIRST"
  };
  const albums = buildAlbums(rawTracks);
  const albumByKey = new Map(albums.map((album) => [album.key, album]));
  const restored = restoreState();

  const state = {
    playlist: restored.playlist,
    activeAlbum: restored.activeAlbum,
    currentId: restored.currentId,
    context: restored.context,
    autoplay: restored.autoplay,
    shuffle: restored.shuffle,
    sortMode: restored.sortMode,
    mobilePanel: restored.mobilePanel,
    wantsPlayback: false,
    attemptedFallback: false,
    dragId: "",
    transitionToken: 0,
    volumeBeforeMute: 0.82
  };

  const audio = document.getElementById("audio");
  const refs = {
    player: document.getElementById("player"),
    nowPreview: document.getElementById("now-preview"),
    ticketLink: document.getElementById("ticket-link"),
    context: document.getElementById("context-readout"),
    status: document.getElementById("player-status"),
    title: document.getElementById("now-title"),
    album: document.getElementById("now-album"),
    position: document.getElementById("now-position"),
    source: document.getElementById("source-link"),
    seek: document.getElementById("seek"),
    scrubFill: document.getElementById("scrub-fill"),
    elapsed: document.getElementById("elapsed"),
    duration: document.getElementById("duration"),
    previous: document.getElementById("previous"),
    play: document.getElementById("play"),
    next: document.getElementById("next"),
    mute: document.getElementById("mute"),
    autoplay: document.getElementById("autoplay"),
    shuffle: document.getElementById("shuffle"),
    resetOrder: document.getElementById("reset-order"),
    resetOrderSecondary: document.getElementById("reset-order-secondary"),
    playlistSort: document.getElementById("playlist-sort"),
    playAlbum: document.getElementById("play-album"),
    playPlaylist: document.getElementById("play-playlist"),
    albumCount: document.getElementById("album-count"),
    songsKicker: document.getElementById("songs-kicker"),
    albumList: document.getElementById("album-list"),
    songList: document.getElementById("song-list"),
    playlistList: document.getElementById("playlist-list"),
    programStatus: document.getElementById("program-status"),
    programCount: document.getElementById("program-count"),
    analysisDialog: document.getElementById("analysis-dialog"),
    analysisClose: document.getElementById("analysis-close"),
    analysisPreview: document.getElementById("analysis-preview"),
    analysisTitle: document.getElementById("analysis-title"),
    analysisAlbum: document.getElementById("analysis-album"),
    analysisVocalStatus: document.getElementById("analysis-vocal-status"),
    analysisVibes: document.getElementById("analysis-vibes"),
    analysisMetrics: document.getElementById("analysis-metrics"),
    transcriptConfidence: document.getElementById("transcript-confidence"),
    transcriptCopy: document.getElementById("transcript-copy"),
    albumTemplate: document.getElementById("album-template"),
    songTemplate: document.getElementById("song-template"),
    playlistTemplate: document.getElementById("playlist-template")
  };

  let statusTimer = 0;
  let analysisRequestToken = 0;

  function buildAlbums(tracks) {
    const records = new Map();
    tracks.forEach((track) => {
      if (!records.has(track.albumKey)) {
        records.set(track.albumKey, {
          key: track.albumKey,
          label: track.album,
          page: track.albumPage,
          preview: track.preview,
          tracks: []
        });
      }
      records.get(track.albumKey).tracks.push(track);
    });
    return Array.from(records.values()).map((album) => ({
      ...album,
      tracks: album.tracks.slice().sort((a, b) => a.sourceIndex - b.sourceIndex || a.index - b.index)
    }));
  }

  function safeStorage(action, fallback) {
    try { return action(); } catch { return fallback; }
  }

  function validPlaylist(order) {
    if (!Array.isArray(order) || order.length !== canonicalOrder.length) return false;
    const unique = new Set(order);
    return unique.size === canonicalOrder.length && canonicalOrder.every((id) => unique.has(id));
  }

  function restoreState() {
    const fallback = {
      playlist: canonicalOrder.slice(),
      activeAlbum: albums[0]?.key || "",
      currentId: canonicalOrder[0],
      context: "playlist",
      autoplay: true,
      shuffle: false,
      sortMode: "custom",
      mobilePanel: "albums"
    };
    const saved = safeStorage(() => JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"), {});
    const playlist = validPlaylist(saved.order) ? saved.order.slice() : fallback.playlist;
    const activeAlbum = albumByKey.has(saved.activeAlbum) ? saved.activeAlbum : fallback.activeAlbum;
    const currentId = trackById.has(saved.currentId) ? saved.currentId : playlist[0];
    return {
      playlist,
      activeAlbum,
      currentId,
      context: saved.context === "album" ? "album" : "playlist",
      autoplay: typeof saved.autoplay === "boolean" ? saved.autoplay : true,
      shuffle: typeof saved.shuffle === "boolean" ? saved.shuffle : false,
      sortMode: Object.hasOwn(sortLabels, saved.sortMode) ? saved.sortMode : "custom",
      mobilePanel: ["albums", "songs", "playlist"].includes(saved.mobilePanel) ? saved.mobilePanel : "albums"
    };
  }

  function saveState() {
    safeStorage(() => localStorage.setItem(STORAGE_KEY, JSON.stringify({
      version: 2,
      order: state.playlist,
      activeAlbum: state.activeAlbum,
      currentId: state.currentId,
      context: state.context,
      autoplay: state.autoplay,
      shuffle: state.shuffle,
      sortMode: state.sortMode,
      mobilePanel: state.mobilePanel
    })));
  }

  function fmt(seconds) {
    if (!Number.isFinite(seconds) || seconds < 0) return "--:--";
    return `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, "0")}`;
  }

  function currentTrack() {
    return trackById.get(state.currentId) || trackById.get(state.playlist[0]) || rawTracks[0];
  }

  function activeQueue() {
    if (state.context === "album") {
      const album = albumByKey.get(currentTrack().albumKey) || albumByKey.get(state.activeAlbum);
      return album?.tracks || [];
    }
    return state.playlist.map((id) => trackById.get(id)).filter(Boolean);
  }

  function queueIndex() {
    return Math.max(0, activeQueue().findIndex((track) => track.id === state.currentId));
  }

  function orderIsCanonical() {
    return state.playlist.every((id, index) => id === canonicalOrder[index]);
  }

  function programLabel() {
    if (orderIsCanonical()) return "TIMESTAMP ORDER / SAVED LOCALLY";
    return `${sortLabels[state.sortMode] || sortLabels.custom} / SAVED LOCALLY`;
  }

  function voiceLabel(status, short = false) {
    const labels = {
      "lyrics-detected": short ? "LYRICS" : "LYRICS DETECTED",
      "vocal-fragment": short ? "VOCAL?" : "VOCAL / SAMPLE",
      "likely-instrumental": short ? "INSTR?" : "LIKELY INSTRUMENTAL",
      unprocessed: "UNPROCESSED"
    };
    return labels[status] || labels.unprocessed;
  }

  function trackAnalysis(id) {
    return analysisById.get(id) || null;
  }

  function analysisLine(track, includeAlbum = true) {
    const record = trackAnalysis(track.id);
    if (!record?.features) return includeAlbum ? track.album : `SIDE ${track.side} / MIX ${String(track.index).padStart(3, "0")}`;
    const parts = [];
    if (includeAlbum) parts.push(track.album);
    parts.push(`${Math.round(record.features.bpm)} BPM`);
    if (record.editorial?.dramaticRole) parts.push(record.editorial.dramaticRole);
    parts.push(voiceLabel(record.voice?.status, true));
    return parts.join(" / ");
  }

  function announce(message, duration = 1500) {
    window.clearTimeout(statusTimer);
    refs.programStatus.textContent = String(message || "").toUpperCase();
    statusTimer = window.setTimeout(() => {
      refs.programStatus.textContent = programLabel();
    }, duration);
  }

  function animateCurrent() {
    state.transitionToken += 1;
    const token = state.transitionToken;
    refs.player.classList.remove("track-change");
    void refs.player.offsetWidth;
    refs.player.classList.add("track-change");
    window.setTimeout(() => {
      if (state.transitionToken === token) refs.player.classList.remove("track-change");
    }, 190);
  }

  function updatePlayer() {
    const track = currentTrack();
    const queue = activeQueue();
    const index = Math.max(0, queue.findIndex((item) => item.id === track.id));
    const contextLabel = state.context === "album" ? track.album : "PLAYLIST";
    animateCurrent();
    refs.nowPreview.src = track.preview || track.artwork;
    refs.nowPreview.alt = `${track.title} isolated ticket artwork`;
    refs.ticketLink.href = track.artwork;
    refs.ticketLink.setAttribute("aria-label", `Open ticket for ${track.title}`);
    refs.title.textContent = track.title;
    refs.album.textContent = track.album;
    refs.album.href = track.albumPage;
    refs.source.href = track.songPage;
    refs.position.textContent = `${String(index + 1).padStart(2, "0")} / ${queue.length}`;
    refs.context.textContent = `${state.context === "album" ? "ALBUM" : "PLAYLIST"} / ${contextLabel} / ${queue.length}`;
    refs.autoplay.textContent = state.autoplay ? "AUTO ON" : "AUTO OFF";
    refs.autoplay.classList.toggle("on", state.autoplay);
    refs.autoplay.setAttribute("aria-pressed", String(state.autoplay));
    refs.shuffle.classList.toggle("on", state.shuffle);
    refs.shuffle.setAttribute("aria-pressed", String(state.shuffle));
    refs.programCount.textContent = `${state.playlist.length} TRACKS / ${albums.length} ALBUMS`;
    updateMediaSession(track);
  }

  function renderAlbums() {
    const scrollTop = refs.albumList.scrollTop;
    const fragment = document.createDocumentFragment();
    albums.forEach((album, index) => {
      const card = refs.albumTemplate.content.firstElementChild.cloneNode(true);
      card.dataset.album = album.key;
      card.classList.toggle("active", album.key === state.activeAlbum);
      const focus = card.querySelector(".album-focus");
      focus.setAttribute("aria-label", `Open ${album.label}`);
      focus.setAttribute("aria-pressed", String(album.key === state.activeAlbum));
      card.querySelector(".album-number").textContent = String(index + 1).padStart(2, "0");
      const image = card.querySelector(".album-preview");
      image.src = album.preview;
      image.alt = "";
      card.querySelector(".album-key").textContent = album.key;
      card.querySelector(".album-title").textContent = album.label;
      card.querySelector(".album-meta").textContent = `${album.tracks.length} selected songs`;
      focus.addEventListener("click", () => selectAlbum(album.key));
      const play = card.querySelector(".album-play");
      play.setAttribute("aria-label", `Play ${album.label}`);
      play.addEventListener("click", () => playAlbum(album.key));
      fragment.append(card);
    });
    refs.albumList.replaceChildren(fragment);
    refs.albumList.scrollTop = scrollTop;
    refs.albumCount.textContent = String(albums.length);
  }

  function renderSongs() {
    const album = albumByKey.get(state.activeAlbum) || albums[0];
    const scrollTop = refs.songList.scrollTop;
    const fragment = document.createDocumentFragment();
    refs.songsKicker.textContent = `${album.label} / ${album.tracks.length}`;
    album.tracks.forEach((track) => {
      const card = refs.songTemplate.content.firstElementChild.cloneNode(true);
      card.dataset.trackId = track.id;
      card.classList.toggle("now-playing", track.id === state.currentId && !!audio.src);
      card.querySelector(".song-number").textContent = String(track.sourceIndex).padStart(2, "0");
      const image = card.querySelector(".song-preview");
      image.src = track.preview;
      image.alt = "";
      card.querySelector(".song-title").textContent = track.title;
      card.querySelector(".song-meta").textContent = analysisLine(track, false);
      const analysisOpen = card.querySelector(".analysis-open");
      analysisOpen.setAttribute("aria-label", `Open analysis for ${track.title}`);
      analysisOpen.addEventListener("click", () => openAnalysis(track.id));
      const play = card.querySelector(".song-play");
      play.textContent = track.id === state.currentId && !audio.paused ? "PAUSE" : "PLAY";
      play.setAttribute("aria-label", `Play ${track.title} in album context`);
      play.addEventListener("click", () => {
        if (track.id === state.currentId && !audio.paused) pauseAudio();
        else playTrack(track.id, "album", true);
      });
      const ticket = card.querySelector(".song-ticket");
      ticket.href = track.artwork;
      ticket.setAttribute("aria-label", `Open ticket for ${track.title}`);
      fragment.append(card);
    });
    refs.songList.replaceChildren(fragment);
    refs.songList.scrollTop = scrollTop;
  }

  function renderPlaylist({ pulseId = "" } = {}) {
    const scrollTop = refs.playlistList.scrollTop;
    const fragment = document.createDocumentFragment();
    state.playlist.forEach((id, index) => {
      const track = trackById.get(id);
      const card = refs.playlistTemplate.content.firstElementChild.cloneNode(true);
      card.dataset.trackId = id;
      card.classList.toggle("now-playing", id === state.currentId && !!audio.src);
      card.classList.toggle("reorder-pulse", id === pulseId);
      card.querySelector(".playlist-position").textContent = String(index + 1).padStart(3, "0");
      const image = card.querySelector(".playlist-preview");
      image.src = track.preview;
      image.alt = "";
      card.querySelector(".playlist-title").textContent = track.title;
      card.querySelector(".playlist-meta").textContent = analysisLine(track, true);
      const analysisOpen = card.querySelector(".analysis-open");
      analysisOpen.setAttribute("aria-label", `Open analysis for ${track.title}`);
      analysisOpen.addEventListener("click", () => openAnalysis(track.id));
      const play = card.querySelector(".playlist-play");
      play.textContent = id === state.currentId && !audio.paused ? "PAUSE" : "PLAY";
      play.setAttribute("aria-label", `Play ${track.title} in playlist context`);
      play.addEventListener("click", () => {
        if (id === state.currentId && !audio.paused) pauseAudio();
        else playTrack(id, "playlist", true);
      });
      const up = card.querySelector(".move-up");
      const down = card.querySelector(".move-down");
      up.disabled = index === 0;
      down.disabled = index === state.playlist.length - 1;
      up.addEventListener("click", () => movePlaylist(id, -1));
      down.addEventListener("click", () => movePlaylist(id, 1));
      card.addEventListener("dragstart", (event) => startDrag(event, id, card));
      card.addEventListener("dragover", (event) => dragOver(event, id, card));
      card.addEventListener("dragleave", () => card.classList.remove("drop-ready"));
      card.addEventListener("drop", (event) => dropTrack(event, id));
      card.addEventListener("dragend", clearDrag);
      fragment.append(card);
    });
    refs.playlistList.replaceChildren(fragment);
    refs.playlistList.scrollTop = scrollTop;
    refs.playlistSort.value = state.sortMode;
  }

  function renderWorkspace(options) {
    renderAlbums();
    renderSongs();
    renderPlaylist(options);
    setMobilePanel(state.mobilePanel, false);
  }

  function addMetric(label, value) {
    const wrapper = document.createElement("div");
    const term = document.createElement("dt");
    const description = document.createElement("dd");
    term.textContent = label;
    description.textContent = value;
    wrapper.append(term, description);
    refs.analysisMetrics.append(wrapper);
  }

  async function openAnalysis(id) {
    const track = trackById.get(id);
    const record = trackAnalysis(id);
    if (!track || !record?.features) {
      announce("Analysis unavailable");
      return;
    }
    const feature = record.features;
    const editorial = record.editorial || {};
    const voice = record.voice || { status: "unprocessed", confidence: 0 };
    analysisRequestToken += 1;
    const requestToken = analysisRequestToken;

    refs.analysisPreview.src = track.preview;
    refs.analysisPreview.alt = `${track.title} isolated artwork`;
    refs.analysisTitle.textContent = track.title;
    refs.analysisAlbum.textContent = track.album;
    refs.analysisVocalStatus.textContent = `${voiceLabel(voice.status)} / ${Math.round((voice.confidence || 0) * 100)}%`;
    refs.analysisVibes.textContent = [
      editorial.dramaticRole,
      editorial.tone,
      ...(editorial.vibes || [])
    ].filter(Boolean).join(" / ");
    refs.analysisMetrics.replaceChildren();
    addMetric("BPM ESTIMATE", `${Math.round(feature.bpm)}`);
    addMetric("PULSE CONF.", `${Math.round(feature.tempoConfidence * 100)}%`);
    addMetric("PACE", `${Math.round((editorial.paceScore || 0) * 100)}`);
    addMetric("ENERGY", `${Math.round((editorial.energyScore || 0) * 100)}`);
    addMetric("DRAMA", `${Math.round((editorial.dramaScore || 0) * 100)}`);
    addMetric("DYNAMICS", `${feature.dynamicRangeDb.toFixed(1)} dB`);
    addMetric("KEY EST.", `${feature.keyEstimate} ${feature.modeEstimate}`);
    addMetric("ENERGY PEAK", `${feature.energyPeakEighth} / 8`);

    refs.transcriptConfidence.textContent = [
      String(voice.language || "unknown").toUpperCase(),
      `${Math.round((voice.averageWordProbability || 0) * 100)}% WORD CONF.`,
      voice.reviewRequired ? "REVIEW" : "DRAFT"
    ].join(" / ");
    if (!refs.analysisDialog.open) refs.analysisDialog.showModal();
    if (voice.transcriptPath) {
      refs.transcriptCopy.textContent = "LOADING TRANSCRIPT";
      try {
        const response = await fetch(voice.transcriptPath);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const transcript = await response.json();
        if (requestToken !== analysisRequestToken) return;
        const lines = (transcript.segments || [])
          .filter((segment) => segment.text)
          .map((segment) => `[${fmt(segment.start)}] ${segment.text}`);
        refs.transcriptCopy.textContent = lines.join("\n\n") || transcript.text || "No transcript text accepted.";
      } catch {
        if (requestToken === analysisRequestToken) refs.transcriptCopy.textContent = "TRANSCRIPT LOAD ERROR";
      }
    } else if (voice.status === "likely-instrumental") {
      refs.transcriptCopy.textContent = "No credible lyrical transcript was found in the distributed scans. Review before confirming instrumental status.";
    } else if (voice.status === "vocal-fragment") {
      refs.transcriptCopy.textContent = "Vocal or sampled-speech evidence was found, but no full transcript is available yet.";
    } else {
      refs.transcriptCopy.textContent = "TRANSCRIPTION PENDING";
    }
  }

  function applyAnalysisSort(mode) {
    if (!Object.hasOwn(sortLabels, mode)) return;
    if (mode === "custom") {
      state.sortMode = "custom";
      saveState();
      announce("Custom order active");
      return;
    }
    const base = canonicalOrder.slice();
    const value = (id, field, fallback = 0) => trackAnalysis(id)?.editorial?.[field] ?? fallback;
    const bpm = (id) => trackAnalysis(id)?.features?.bpm ?? Number.POSITIVE_INFINITY;
    const voice = (id) => trackAnalysis(id)?.voice?.status || "unprocessed";
    let ordered;
    if (mode === "drama") {
      ordered = (analysis.suggestedOrder || []).slice();
    } else if (mode === "pace-up") {
      ordered = base.sort((a, b) => value(a, "paceScore", 2) - value(b, "paceScore", 2));
    } else if (mode === "pace-down") {
      ordered = base.sort((a, b) => value(b, "paceScore", -1) - value(a, "paceScore", -1));
    } else if (mode === "energy") {
      ordered = base.sort((a, b) => value(b, "energyScore", -1) - value(a, "energyScore", -1));
    } else if (mode === "bpm") {
      ordered = base.sort((a, b) => bpm(a) - bpm(b));
    } else {
      const ranks = mode === "lyrics"
        ? { "lyrics-detected": 0, "vocal-fragment": 1, "likely-instrumental": 2, unprocessed: 3 }
        : { "likely-instrumental": 0, "vocal-fragment": 1, "lyrics-detected": 2, unprocessed: 3 };
      ordered = base.sort((a, b) => ranks[voice(a)] - ranks[voice(b)]);
    }
    const unique = [...new Set(ordered.filter((id) => trackById.has(id)))];
    canonicalOrder.forEach((id) => { if (!unique.includes(id)) unique.push(id); });
    if (!validPlaylist(unique)) {
      announce("Analysis order unavailable");
      refs.playlistSort.value = state.sortMode;
      return;
    }
    state.playlist = unique;
    state.sortMode = mode;
    saveState();
    renderPlaylist();
    updatePlayer();
    refs.playlistList.scrollTop = 0;
    announce(`${sortLabels[mode]} applied`);
  }

  function setMobilePanel(panel, save = true) {
    state.mobilePanel = panel;
    document.querySelectorAll("[data-mobile-panel]").forEach((button) => {
      const active = button.dataset.mobilePanel === panel;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    document.querySelectorAll("[data-panel]").forEach((column) => {
      column.classList.toggle("mobile-active", column.dataset.panel === panel);
    });
    if (save) saveState();
  }

  function selectAlbum(key) {
    if (!albumByKey.has(key)) return;
    state.activeAlbum = key;
    saveState();
    renderAlbums();
    renderSongs();
    setMobilePanel("songs");
    announce(`${albumByKey.get(key).label} opened`);
  }

  function playAlbum(key) {
    const album = albumByKey.get(key);
    if (!album?.tracks.length) return;
    state.activeAlbum = key;
    playTrack(album.tracks[0].id, "album", true);
    setMobilePanel("songs");
    announce(`Playing ${album.label}`);
  }

  function playPlaylist() {
    if (!state.playlist.length) return;
    playTrack(state.playlist[0], "playlist", true);
    setMobilePanel("playlist");
    announce("Playing custom playlist");
  }

  function playTrack(id, context, autoplay) {
    const track = trackById.get(id);
    if (!track) return;
    state.context = context === "album" ? "album" : "playlist";
    state.currentId = id;
    if (state.context === "album") state.activeAlbum = track.albumKey;
    state.attemptedFallback = false;
    audio.src = track.audio;
    audio.load();
    refs.seek.value = "0";
    refs.scrubFill.style.width = "0%";
    refs.elapsed.textContent = "0:00";
    refs.duration.textContent = "--:--";
    refs.status.textContent = autoplay ? "LOADING" : "READY";
    updatePlayer();
    renderWorkspace();
    saveState();
    if (autoplay) playAudio();
  }

  async function playAudio() {
    try {
      if (!audio.src) playTrack(state.currentId, state.context, false);
      state.wantsPlayback = true;
      refs.status.textContent = "LOADING";
      await audio.play();
    } catch (error) {
      state.wantsPlayback = false;
      refs.status.textContent = error?.name === "NotAllowedError" ? "PRESS PLAY" : "PLAY ERROR";
    }
  }

  function pauseAudio() {
    state.wantsPlayback = false;
    audio.pause();
  }

  function togglePlay() {
    if (audio.paused) playAudio();
    else pauseAudio();
  }

  function movePlaylist(id, delta) {
    const index = state.playlist.indexOf(id);
    const target = index + delta;
    if (index < 0 || target < 0 || target >= state.playlist.length) return;
    const next = state.playlist.slice();
    const [moved] = next.splice(index, 1);
    next.splice(target, 0, moved);
    state.playlist = next;
    state.sortMode = "custom";
    saveState();
    renderPlaylist({ pulseId: id });
    updatePlayer();
    announce(`${trackById.get(id).title} moved to ${target + 1}`);
  }

  function reorderPlaylist(sourceId, targetId) {
    if (sourceId === targetId) return;
    const next = state.playlist.filter((id) => id !== sourceId);
    const targetIndex = next.indexOf(targetId);
    if (targetIndex < 0) return;
    next.splice(targetIndex, 0, sourceId);
    state.playlist = next;
    state.sortMode = "custom";
    saveState();
    renderPlaylist({ pulseId: sourceId });
    updatePlayer();
    announce(`${trackById.get(sourceId).title} moved to ${targetIndex + 1}`);
  }

  function startDrag(event, id, card) {
    if (!event.target.closest(".drag-handle")) {
      event.preventDefault();
      return;
    }
    state.dragId = id;
    card.classList.add("dragging");
    event.dataTransfer.effectAllowed = "move";
    event.dataTransfer.setData("text/plain", id);
  }

  function dragOver(event, targetId, card) {
    if (!state.dragId || state.dragId === targetId) return;
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
    card.classList.add("drop-ready");
  }

  function dropTrack(event, targetId) {
    event.preventDefault();
    const sourceId = state.dragId || event.dataTransfer.getData("text/plain");
    clearDrag();
    reorderPlaylist(sourceId, targetId);
  }

  function clearDrag() {
    state.dragId = "";
    document.querySelectorAll(".dragging, .drop-ready").forEach((card) => {
      card.classList.remove("dragging", "drop-ready");
    });
  }

  function resetOrder() {
    if (orderIsCanonical()) {
      announce("Playlist already in timestamp order");
      return;
    }
    if (!window.confirm("Restore the original timestamp order?")) return;
    state.playlist = canonicalOrder.slice();
    state.sortMode = "custom";
    saveState();
    renderPlaylist();
    updatePlayer();
    announce("Timestamp order restored");
  }

  function randomQueueTrack(queue) {
    if (queue.length < 2) return queue[0];
    let candidate = currentTrack();
    while (candidate.id === state.currentId) candidate = queue[Math.floor(Math.random() * queue.length)];
    return candidate;
  }

  function nextTrack(fromEnded = false) {
    const queue = activeQueue();
    if (!queue.length) return;
    if (fromEnded && !state.autoplay) {
      refs.status.textContent = "READY";
      return;
    }
    const current = queueIndex();
    const next = state.shuffle ? randomQueueTrack(queue) : queue[current + 1];
    if (next) playTrack(next.id, state.context, true);
    else if (!fromEnded) playTrack(queue[0].id, state.context, true);
    else refs.status.textContent = "QUEUE COMPLETE";
  }

  function previousTrack() {
    if (audio.currentTime > 3) {
      audio.currentTime = 0;
      return;
    }
    const queue = activeQueue();
    if (!queue.length) return;
    const current = queueIndex();
    const previous = queue[current - 1] || queue[queue.length - 1];
    playTrack(previous.id, state.context, true);
  }

  function updateProgress() {
    const progress = Number.isFinite(audio.duration) && audio.duration > 0
      ? Math.max(0, Math.min(1, audio.currentTime / audio.duration))
      : 0;
    refs.elapsed.textContent = fmt(audio.currentTime);
    refs.duration.textContent = fmt(audio.duration);
    refs.seek.value = String(Math.round(progress * 1000));
    refs.scrubFill.style.width = `${progress * 100}%`;
  }

  function updateMediaSession(track) {
    if (!("mediaSession" in navigator) || !("MediaMetadata" in window)) return;
    navigator.mediaSession.metadata = new MediaMetadata({
      title: track.title,
      artist: track.album,
      album: mix.title,
      artwork: [{ src: new URL(track.preview || track.artwork, window.location.href).href, sizes: "320x320", type: "image/webp" }]
    });
  }

  document.querySelectorAll("[data-mobile-panel]").forEach((button) => {
    button.addEventListener("click", () => setMobilePanel(button.dataset.mobilePanel));
  });
  refs.playAlbum.addEventListener("click", () => playAlbum(state.activeAlbum));
  refs.playPlaylist.addEventListener("click", playPlaylist);
  refs.previous.addEventListener("click", previousTrack);
  refs.play.addEventListener("click", togglePlay);
  refs.next.addEventListener("click", () => nextTrack(false));
  refs.resetOrder.addEventListener("click", resetOrder);
  refs.resetOrderSecondary.addEventListener("click", resetOrder);
  refs.playlistSort.addEventListener("change", () => applyAnalysisSort(refs.playlistSort.value));
  refs.analysisClose.addEventListener("click", () => refs.analysisDialog.close());
  refs.analysisDialog.addEventListener("click", (event) => {
    if (event.target === refs.analysisDialog) refs.analysisDialog.close();
  });
  refs.autoplay.addEventListener("click", () => {
    state.autoplay = !state.autoplay;
    updatePlayer();
    saveState();
    announce(`Autoplay ${state.autoplay ? "on" : "off"}`);
  });
  refs.shuffle.addEventListener("click", () => {
    state.shuffle = !state.shuffle;
    updatePlayer();
    saveState();
    announce(`Shuffle ${state.shuffle ? "on" : "off"}`);
  });
  refs.mute.addEventListener("click", () => {
    if (audio.muted || audio.volume === 0) {
      audio.muted = false;
      audio.volume = state.volumeBeforeMute || 0.82;
    } else {
      state.volumeBeforeMute = audio.volume;
      audio.muted = true;
    }
    refs.mute.textContent = audio.muted ? "MUTE" : "VOL";
    refs.mute.setAttribute("aria-pressed", String(audio.muted));
    refs.mute.setAttribute("aria-label", audio.muted ? "Unmute audio" : "Mute audio");
  });
  refs.seek.addEventListener("input", () => {
    if (Number.isFinite(audio.duration)) audio.currentTime = (Number(refs.seek.value) / 1000) * audio.duration;
  });

  audio.addEventListener("play", () => {
    state.wantsPlayback = true;
    refs.play.textContent = "PAUSE";
    refs.play.setAttribute("aria-label", "Pause");
    refs.status.textContent = "PLAYING";
    renderSongs();
    renderPlaylist();
  });
  audio.addEventListener("pause", () => {
    refs.play.textContent = "PLAY";
    refs.play.setAttribute("aria-label", "Play");
    if (!audio.ended && refs.status.textContent !== "QUEUE COMPLETE") refs.status.textContent = "PAUSED";
    renderSongs();
    renderPlaylist();
  });
  audio.addEventListener("waiting", () => { refs.status.textContent = "BUFFERING"; });
  audio.addEventListener("canplay", () => { if (!audio.paused) refs.status.textContent = "PLAYING"; });
  audio.addEventListener("timeupdate", updateProgress);
  audio.addEventListener("durationchange", updateProgress);
  audio.addEventListener("ended", () => nextTrack(true));
  audio.addEventListener("error", () => {
    const track = currentTrack();
    if (!state.attemptedFallback && track.sourceAudio && track.sourceAudio !== track.audio) {
      state.attemptedFallback = true;
      const shouldResume = state.wantsPlayback;
      audio.src = track.sourceAudio;
      audio.load();
      if (shouldResume) playAudio();
      return;
    }
    refs.status.textContent = "MEDIA ERROR";
  });

  document.addEventListener("keydown", (event) => {
    const target = event.target;
    if (target instanceof HTMLInputElement || target instanceof HTMLButtonElement || target instanceof HTMLAnchorElement) return;
    if (event.code === "Space") {
      event.preventDefault();
      togglePlay();
    } else if (event.code === "ArrowRight") nextTrack(false);
    else if (event.code === "ArrowLeft") previousTrack();
  });

  if ("mediaSession" in navigator) {
    const handlers = {
      play: playAudio,
      pause: pauseAudio,
      previoustrack: previousTrack,
      nexttrack: () => nextTrack(false),
      seekto: (details) => {
        if (details.seekTime != null) audio.currentTime = details.seekTime;
      }
    };
    Object.entries(handlers).forEach(([action, handler]) => {
      try { navigator.mediaSession.setActionHandler(action, handler); } catch { /* Unsupported action. */ }
    });
  }

  audio.volume = 0.82;
  state.volumeBeforeMute = audio.volume;
  updatePlayer();
  renderWorkspace();
  refs.programStatus.textContent = programLabel();
  setMobilePanel(state.mobilePanel, false);
})();
