(() => {
  "use strict";

  const manifest = window.ALL_TIME_EMBEDDED_MANIFEST;
  const intelligence = window.ANY_TIME_INTELLIGENCE;
  if (!manifest?.albums || !intelligence?.records) return;

  const STORAGE_KEY = "anyTimeLab.v1";
  const RESULT_STEP = 80;
  const MODE_LABELS = {
    all: "ALL FIELDS",
    words: "TRANSCRIPT WORDS",
    themes: "THEME RELATIONS",
    tempo: "ANALYZED TEMPO",
    genre: "GENRE SIGNALS"
  };
  const MODE_PLACEHOLDERS = {
    all: "SEARCH TITLE, ALBUM, SIGNAL, OR LYRICS",
    words: "SEARCH ACTUAL TRANSCRIPT WORDS",
    themes: "SEARCH THEMES, IMAGES, OR IDEAS",
    tempo: "ENTER A TARGET BPM OR USE BPM RANGE",
    genre: "SEARCH DUB, FUNK, SOUL, BREAKS, RAP..."
  };
  const GENRE_RULES = [
    ["DUB", ["dub", "low-end", "bass"]],
    ["FUNK", ["funk", "afro-funk"]],
    ["SOUL", ["soul"]],
    ["GOSPEL", ["gospel", "hymn", "hymns", "sermon", "sermons"]],
    ["BLUES", ["blues"]],
    ["RAP / CYPHER", ["rap", "cypher", "trap"]],
    ["BREAKS / BOUNCE", ["break", "breaks", "bounce", "footwork", "passinho"]],
    ["CUMBIA / KUDURO", ["cumbia", "kuduro"]],
    ["FOLK", ["folk", "banjo", "strings"]],
    ["INDUSTRIAL", ["industrial", "machine", "steel", "infrastructure"]],
    ["AMBIENT / DRONE", ["ambient", "drone", "drones", "drift", "void"]],
    ["POP", ["pop"]],
    ["RITUAL", ["ritual", "rituals", "cathedral", "shrine"]],
    ["FIELD / NOIR", ["field", "fieldwork", "noir"]]
  ];
  const STOP_WORDS = new Set(["a", "an", "and", "at", "for", "from", "in", "of", "on", "the", "to", "with"]);

  const refs = {
    player: document.getElementById("player"),
    artLink: document.getElementById("now-art-link"),
    art: document.getElementById("now-art"),
    context: document.getElementById("context-readout"),
    addCurrent: document.getElementById("add-current"),
    undo: document.getElementById("undo"),
    playerState: document.getElementById("player-state"),
    title: document.getElementById("now-title"),
    meta: document.getElementById("now-meta"),
    inspectCurrent: document.getElementById("inspect-current"),
    elapsed: document.getElementById("elapsed"),
    duration: document.getElementById("duration"),
    seek: document.getElementById("seek"),
    previous: document.getElementById("previous"),
    play: document.getElementById("play"),
    next: document.getElementById("next"),
    playSet: document.getElementById("play-set"),
    search: document.getElementById("search"),
    clearSearch: document.getElementById("clear-search"),
    coverage: document.getElementById("coverage"),
    albumFilter: document.getElementById("album-filter"),
    genreFilter: document.getElementById("genre-filter"),
    vocalFilter: document.getElementById("vocal-filter"),
    themeFilter: document.getElementById("theme-filter"),
    bpmMin: document.getElementById("bpm-min"),
    bpmMax: document.getElementById("bpm-max"),
    sort: document.getElementById("sort"),
    resetFilters: document.getElementById("reset-filters"),
    resultScope: document.getElementById("result-scope"),
    resultCount: document.getElementById("result-count"),
    results: document.getElementById("results"),
    loadMore: document.getElementById("load-more"),
    setRuntime: document.getElementById("set-runtime"),
    setList: document.getElementById("set-list"),
    exportSet: document.getElementById("export-set"),
    clearSet: document.getElementById("clear-set"),
    metricTracks: document.getElementById("metric-tracks"),
    metricBpm: document.getElementById("metric-bpm"),
    metricVoice: document.getElementById("metric-voice"),
    metricFlags: document.getElementById("metric-flags"),
    energyArc: document.getElementById("energy-arc"),
    mobileSetCount: document.getElementById("mobile-set-count"),
    status: document.getElementById("status"),
    coverageReadout: document.getElementById("coverage-readout"),
    detail: document.getElementById("detail-dialog"),
    detailClose: document.getElementById("detail-close"),
    detailArt: document.getElementById("detail-art"),
    detailState: document.getElementById("detail-state"),
    detailTitle: document.getElementById("detail-title"),
    detailAlbum: document.getElementById("detail-album"),
    detailPlay: document.getElementById("detail-play"),
    detailAdd: document.getElementById("detail-add"),
    detailSource: document.getElementById("detail-source"),
    detailMetrics: document.getElementById("detail-metrics"),
    detailConfidence: document.getElementById("detail-confidence"),
    detailEvidence: document.getElementById("detail-evidence"),
    transcriptState: document.getElementById("transcript-state"),
    transcriptCopy: document.getElementById("transcript-copy"),
    relatedTracks: document.getElementById("related-tracks"),
    audio: document.getElementById("audio")
  };

  function canonicalPage(value) {
    let page = String(value || "").replaceAll("\\", "/");
    while (page.startsWith("../")) page = page.slice(3);
    return page.replace(/^\.\//, "").replace(/^\//, "");
  }

  function normalize(value) {
    return String(value || "")
      .normalize("NFKD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  }

  function tokens(value) {
    return normalize(value).split(/\s+/).filter((token) => token && !STOP_WORDS.has(token));
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function assetPath(source) {
    if (!source) return "";
    if (/^(https?:|data:|blob:)/i.test(source)) return source;
    return `./${String(source).replace(/^\.\//, "")}`;
  }

  function bestDerivative(entry, kind) {
    return entry?.derivatives?.[kind]?.webp
      || entry?.derivatives?.thumb?.webp
      || entry?.source
      || "";
  }

  function audioSource(entry) {
    return entry?.derivatives?.stream?.mp3
      || entry?.derivatives?.fallback?.mp3
      || entry?.source
      || "";
  }

  function genreSignals(text) {
    const haystack = ` ${normalize(text)} `;
    return GENRE_RULES
      .filter(([, termsList]) => termsList.some((term) => haystack.includes(` ${normalize(term)} `)))
      .map(([label]) => label);
  }

  const albums = Object.values(manifest.albums).map((album) => ({
    key: album.key,
    label: album.label || album.key,
    signal: album.subtitle || "",
    cover: bestDerivative(album.cover || album.defaultTrackArt, "thumb"),
    defaultArt: bestDerivative(album.defaultTrackArt || album.cover, "thumb"),
    tracks: album.tracks || []
  }));
  const albumByKey = new Map(albums.map((album) => [album.key, album]));
  const themeById = new Map((intelligence.themes || []).map((theme) => [theme.id, theme]));
  const tracks = [];

  albums.forEach((album) => {
    album.tracks.forEach((sourceTrack) => {
      const page = canonicalPage(sourceTrack.songPage);
      const intel = intelligence.records[page] || null;
      const art = bestDerivative(sourceTrack.art || {}, "thumb") || album.defaultArt || album.cover;
      const transcript = (intel?.segments || []).map((segment) => segment.text).join(" ");
      const genres = genreSignals(`${album.signal} ${sourceTrack.title}`);
      const themeText = (intel?.themes || []).map((id) => {
        const theme = themeById.get(id);
        return theme ? `${theme.title} ${theme.thesis}` : id;
      }).join(" ");
      tracks.push({
        id: page || `${album.key}:${sourceTrack.index}`,
        page,
        albumKey: album.key,
        albumLabel: album.label,
        albumSignal: album.signal,
        albumCover: album.cover,
        index: sourceTrack.index,
        title: sourceTrack.title || sourceTrack.file || "Untitled",
        audio: audioSource(sourceTrack.audio || { source: sourceTrack.source }),
        sourceAudio: sourceTrack.audio?.source || sourceTrack.source || "",
        art,
        runtime: Number(sourceTrack.audio?.durationSeconds)
          || Number(intelligence.runtimeByPage?.[page])
          || Number(intel?.durationSeconds)
          || null,
        intel,
        genres,
        transcript,
        search: {
          title: normalize(sourceTrack.title),
          album: normalize(album.label),
          signal: normalize(album.signal),
          transcript: normalize(transcript),
          genre: normalize(genres.join(" ")),
          theme: normalize(themeText)
        },
        libraryIndex: tracks.length
      });
    });
  });

  const trackById = new Map(tracks.map((track) => [track.id, track]));
  const allGenres = [...new Set(tracks.flatMap((track) => track.genres))].sort();
  let resultRecords = [];
  let detailTrackId = "";
  let statusTimer = 0;
  let draggedId = "";
  let movingId = "";
  let isScrubbing = false;
  let attemptedFallback = false;

  const stored = restoreState();
  const state = {
    mode: stored.mode,
    query: stored.query,
    album: stored.album,
    genre: stored.genre,
    vocal: stored.vocal,
    theme: stored.theme,
    bpmMin: stored.bpmMin,
    bpmMax: stored.bpmMax,
    sort: stored.sort,
    setIds: stored.setIds,
    currentId: stored.currentId,
    playContext: stored.playContext,
    resultQueueIds: [],
    resultLimit: RESULT_STEP,
    mobilePanel: stored.mobilePanel,
    history: []
  };

  function restoreState() {
    const fallback = {
      mode: "all", query: "", album: "", genre: "", vocal: "", theme: "",
      bpmMin: "", bpmMax: "", sort: "relevance", setIds: [], currentId: "",
      playContext: "results", mobilePanel: "discover"
    };
    try {
      const raw = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
      const setIds = Array.isArray(raw.setIds)
        ? [...new Set(raw.setIds.filter((id) => trackById.has(id)))]
        : [];
      return {
        ...fallback,
        ...raw,
        mode: Object.hasOwn(MODE_LABELS, raw.mode) ? raw.mode : fallback.mode,
        sort: ["relevance", "bpm-up", "bpm-down", "energy", "album", "title"].includes(raw.sort) ? raw.sort : fallback.sort,
        setIds,
        currentId: trackById.has(raw.currentId) ? raw.currentId : "",
        playContext: raw.playContext === "set" ? "set" : "results",
        mobilePanel: raw.mobilePanel === "set" ? "set" : "discover"
      };
    } catch {
      return fallback;
    }
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        version: 1,
        mode: state.mode,
        query: state.query,
        album: state.album,
        genre: state.genre,
        vocal: state.vocal,
        theme: state.theme,
        bpmMin: state.bpmMin,
        bpmMax: state.bpmMax,
        sort: state.sort,
        setIds: state.setIds,
        currentId: state.currentId,
        playContext: state.playContext,
        mobilePanel: state.mobilePanel
      }));
    } catch {
      // Local storage is optional.
    }
  }

  function fmt(seconds) {
    if (!Number.isFinite(seconds) || seconds < 0) return "--:--";
    return `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, "0")}`;
  }

  function shortNumber(value) {
    return Number.isFinite(value) ? String(Math.round(value)) : "—";
  }

  function voiceStatus(track) {
    return track.intel?.voice?.status || "unknown";
  }

  function voiceShort(track) {
    const labels = {
      "lyrics-detected": "LYRICS",
      "likely-instrumental": "INSTR",
      "vocal-fragment": "VOCAL?",
      unknown: "VOICE —"
    };
    return labels[voiceStatus(track)] || labels.unknown;
  }

  function announce(message, duration = 1800) {
    window.clearTimeout(statusTimer);
    refs.status.textContent = String(message || "READY").toUpperCase();
    statusTimer = window.setTimeout(() => {
      refs.status.textContent = `${MODE_LABELS[state.mode]} / ${resultRecords.length} MATCHES`;
    }, duration);
  }

  function pushHistory() {
    state.history.push(state.setIds.slice());
    if (state.history.length > 24) state.history.shift();
    refs.undo.disabled = false;
  }

  function themeRelation(track, theme) {
    if (!theme) return { score: 0, curated: false, terms: [] };
    const curated = track.intel?.themes?.includes(theme.id) || false;
    const field = `${track.search.title} ${track.search.signal} ${track.search.transcript}`;
    const matches = theme.terms.filter((term) => field.includes(normalize(term)));
    return { score: (curated ? 20 : 0) + Math.min(8, matches.length), curated, terms: matches.slice(0, 4) };
  }

  function transcriptMatch(track, queryTokens) {
    if (!track.intel?.segments?.length || !queryTokens.length) return null;
    return track.intel.segments.find((segment) => {
      const segmentText = normalize(segment.text);
      return queryTokens.some((token) => segmentText.includes(token));
    }) || null;
  }

  function evaluateTrack(track) {
    const reasons = [];
    let score = 0;
    if (state.album && track.albumKey !== state.album) return null;
    if (state.genre && !track.genres.includes(state.genre)) return null;
    const voice = voiceStatus(track);
    if (state.vocal && voice !== state.vocal) return null;

    const bpm = Number(track.intel?.bpm);
    const bpmMin = Number(state.bpmMin);
    const bpmMax = Number(state.bpmMax);
    if (state.bpmMin && (!Number.isFinite(bpm) || bpm < bpmMin)) return null;
    if (state.bpmMax && (!Number.isFinite(bpm) || bpm > bpmMax)) return null;
    if (state.bpmMin || state.bpmMax) reasons.push(`BPM ${shortNumber(bpm)}`);

    if (state.genre) {
      score += 10;
      reasons.push(`GENRE SIGNAL: ${state.genre}`);
    }

    const selectedTheme = themeById.get(state.theme);
    if (selectedTheme) {
      const relation = themeRelation(track, selectedTheme);
      if (!relation.score) return null;
      score += relation.score;
      reasons.push(relation.curated ? `CURATED: ${selectedTheme.title}` : `THEME: ${relation.terms.join(" / ")}`);
    }

    const query = normalize(state.query);
    const queryTokens = tokens(query);
    const targetBpm = state.mode === "tempo" ? Number(query) : NaN;

    if (state.mode === "words" && !track.search.transcript) return null;
    if (state.mode === "tempo" && !Number.isFinite(bpm)) return null;
    if (state.mode === "genre" && !track.genres.length) return null;

    if (state.mode === "themes" && !queryTokens.length && !selectedTheme) {
      const relations = intelligence.themes.map((theme) => ({ theme, ...themeRelation(track, theme) }));
      const strongest = relations.sort((a, b) => b.score - a.score)[0];
      if (!strongest?.score) return null;
      score += strongest.score;
      reasons.push(strongest.curated ? `CURATED: ${strongest.theme.title}` : `THEME: ${strongest.terms.join(" / ")}`);
    }

    if (state.mode === "tempo" && Number.isFinite(targetBpm)) {
      const variants = [bpm / 2, bpm, bpm * 2].filter((value) => value >= 60 && value <= 200);
      const delta = Math.min(...variants.map((value) => Math.abs(value - targetBpm)));
      score += Math.max(0, 30 - delta);
      reasons.push(`${shortNumber(bpm)} BPM / Δ${Math.round(delta)}`);
    } else if (queryTokens.length) {
      const fields = state.mode === "words"
        ? [["WORDS", track.search.transcript, 10]]
        : state.mode === "themes"
          ? [["THEME", track.search.theme, 9], ["SIGNAL", track.search.signal, 7], ["TITLE", track.search.title, 6], ["WORDS", track.search.transcript, 4]]
          : state.mode === "genre"
            ? [["GENRE", track.search.genre, 10], ["SIGNAL", track.search.signal, 7], ["TITLE", track.search.title, 4]]
            : [["TITLE", track.search.title, 12], ["ALBUM", track.search.album, 8], ["SIGNAL", track.search.signal, 7], ["GENRE", track.search.genre, 7], ["THEME", track.search.theme, 6], ["WORDS", track.search.transcript, 5]];

      for (const token of queryTokens) {
        const matches = fields.filter(([, field]) => field.includes(token));
        if (!matches.length) return null;
        const [label, , weight] = matches.sort((a, b) => b[2] - a[2])[0];
        score += weight;
        if (!reasons.some((reason) => reason.startsWith(`${label}:`))) reasons.push(`${label}: ${token}`);
      }
      fields.forEach(([label, field, weight]) => {
        if (query.length > 2 && field.includes(query)) {
          score += weight * 0.7;
          if (!reasons.some((reason) => reason.startsWith(`${label}:`))) reasons.push(`${label}: ${query}`);
        }
      });
    }

    if (!queryTokens.length && state.mode === "all" && !selectedTheme && !state.genre && !state.bpmMin && !state.bpmMax && !state.vocal && !state.album) {
      score = -track.libraryIndex / 10000;
      reasons.push(track.albumSignal ? `SIGNAL: ${track.albumSignal.split("/")[0].trim()}` : "TITLE INDEXED");
    } else {
      if (track.intel?.bpm) score += 0.25;
      if (track.intel?.segments?.length) score += 0.2;
    }

    const segment = transcriptMatch(track, queryTokens);
    if (segment) reasons.push(`WORDS @ ${fmt(segment.start)}`);
    return { track, score, reasons: [...new Set(reasons)].slice(0, 4), segment };
  }

  function sortResults(records) {
    const sort = state.sort;
    const unknown = Number.POSITIVE_INFINITY;
    return records.sort((a, b) => {
      if (sort === "bpm-up") return (a.track.intel?.bpm ?? unknown) - (b.track.intel?.bpm ?? unknown);
      if (sort === "bpm-down") return (b.track.intel?.bpm ?? -1) - (a.track.intel?.bpm ?? -1);
      if (sort === "energy") return (b.track.intel?.energy ?? -1) - (a.track.intel?.energy ?? -1);
      if (sort === "album") return a.track.albumLabel.localeCompare(b.track.albumLabel) || a.track.index - b.track.index;
      if (sort === "title") return a.track.title.localeCompare(b.track.title);
      return b.score - a.score || a.track.libraryIndex - b.track.libraryIndex;
    });
  }

  function refreshResults(resetLimit = false) {
    if (resetLimit) state.resultLimit = RESULT_STEP;
    resultRecords = sortResults(tracks.map(evaluateTrack).filter(Boolean));
    state.resultQueueIds = resultRecords.map((record) => record.track.id);
    renderControls();
    renderResults();
    saveState();
  }

  function trackMeta(track) {
    const parts = [track.albumLabel];
    if (track.intel?.bpm) parts.push(`${Math.round(track.intel.bpm)} BPM`);
    if (track.intel?.role) parts.push(track.intel.role);
    parts.push(voiceShort(track));
    return parts.join(" / ");
  }

  function resultEvidence(record) {
    if (!record.reasons.length) return "TITLE INDEXED";
    return record.reasons.join(" / ");
  }

  function renderResults() {
    const shown = resultRecords.slice(0, state.resultLimit);
    refs.resultCount.textContent = `${shown.length} / ${resultRecords.length}`;
    refs.resultScope.textContent = MODE_LABELS[state.mode];
    if (!shown.length) {
      refs.results.innerHTML = `<li class="empty-state">NO MATCHES IN THE VISIBLE EVIDENCE</li>`;
    } else {
      refs.results.innerHTML = shown.map((record, index) => {
        const track = record.track;
        const committed = state.setIds.includes(track.id);
        const playing = state.currentId === track.id && !refs.audio.paused;
        return `
          <li class="result-card ${committed ? "committed" : ""} ${playing ? "playing" : ""}" data-track="${escapeHtml(track.id)}">
            <span class="card-number">${String(index + 1).padStart(3, "0")}</span>
            <img class="card-art" src="${escapeHtml(assetPath(track.art))}" alt="" loading="lazy" decoding="async" />
            <button class="card-copy" type="button" data-action="detail">
              <strong class="card-title">${escapeHtml(track.title)}</strong>
              <span class="card-meta">${escapeHtml(trackMeta(track))}</span>
              <span class="card-evidence">${escapeHtml(resultEvidence(record))}</span>
            </button>
            <span class="card-actions">
              <button type="button" data-action="play" title="Play ${escapeHtml(track.title)}" aria-label="Play ${escapeHtml(track.title)}">▶</button>
              <button type="button" data-action="add" title="${committed ? "Already in set" : "Add to set"}" aria-label="${committed ? "Already in set" : `Add ${escapeHtml(track.title)} to set`}" ${committed ? "disabled" : ""}>${committed ? "✓" : "+"}</button>
            </span>
          </li>`;
      }).join("");
    }
    refs.loadMore.hidden = shown.length >= resultRecords.length;
    refs.loadMore.textContent = `SHOW ${Math.min(RESULT_STEP, resultRecords.length - shown.length)} MORE`;
  }

  function transitionBetween(previous, track) {
    if (!previous) return { note: "OPENING POSITION", flagged: false };
    const first = Number(previous.intel?.bpm);
    const second = Number(track.intel?.bpm);
    const notes = [];
    let flagged = false;
    if (Number.isFinite(first) && Number.isFinite(second)) {
      const pairs = [];
      [first / 2, first, first * 2].filter((value) => value >= 60 && value <= 200).forEach((a) => {
        [second / 2, second, second * 2].filter((value) => value >= 60 && value <= 200).forEach((b) => pairs.push([Math.abs(a - b), a, b]));
      });
      const [delta, from, to] = pairs.sort((a, b) => a[0] - b[0])[0];
      notes.push(`${Math.round(from)}→${Math.round(to)} BPM`);
      if (delta > 18) flagged = true;
    } else {
      notes.push("BPM —");
    }
    const firstEnergy = Number(previous.intel?.energy);
    const secondEnergy = Number(track.intel?.energy);
    if (Number.isFinite(firstEnergy) && Number.isFinite(secondEnergy)) {
      const delta = secondEnergy - firstEnergy;
      notes.push(`E ${delta >= 0 ? "+" : ""}${Math.round(delta * 100)}`);
      if (Math.abs(delta) > 0.32) flagged = true;
    } else {
      notes.push("ENERGY —");
    }
    return { note: notes.join(" / "), flagged };
  }

  function setTracks() {
    return state.setIds.map((id) => trackById.get(id)).filter(Boolean);
  }

  function renderSet() {
    const list = setTracks();
    let previous = null;
    let flags = 0;
    const transitions = new Map();
    list.forEach((track) => {
      const transition = transitionBetween(previous, track);
      transitions.set(track.id, transition);
      if (transition.flagged) flags += 1;
      previous = track;
    });

    if (!list.length) {
      refs.setList.innerHTML = `<li class="empty-state">ADD CANDIDATES FROM DISCOVER</li>`;
    } else {
      refs.setList.innerHTML = list.map((track, index) => {
        const transition = transitions.get(track.id);
        const playing = state.currentId === track.id && !refs.audio.paused;
        return `
          <li class="set-card ${transition.flagged ? "flagged" : ""} ${playing ? "playing" : ""} ${movingId === track.id ? "moving" : ""}" draggable="true" data-track="${escapeHtml(track.id)}">
            <button class="set-position" type="button" data-action="move" title="Move track">${String(index + 1).padStart(2, "0")}</button>
            <img class="card-art" src="${escapeHtml(assetPath(track.art))}" alt="" loading="lazy" decoding="async" />
            <button class="card-copy" type="button" data-action="detail">
              <strong class="card-title">${escapeHtml(track.title)}</strong>
              <span class="card-meta">${escapeHtml(trackMeta(track))}</span>
              <span class="transition-note">${escapeHtml(transition.note)}</span>
            </button>
            <span class="card-actions set-actions">
              <button class="move-up" type="button" data-action="up" title="Move earlier" aria-label="Move ${escapeHtml(track.title)} earlier" ${index === 0 ? "disabled" : ""}>↑</button>
              <button type="button" data-action="play" title="Play ${escapeHtml(track.title)}" aria-label="Play ${escapeHtml(track.title)}">▶</button>
              <button class="move-down" type="button" data-action="down" title="Move later" aria-label="Move ${escapeHtml(track.title)} later" ${index === list.length - 1 ? "disabled" : ""}>↓</button>
              <button type="button" data-action="cut" title="Cut from set" aria-label="Cut ${escapeHtml(track.title)} from set">×</button>
            </span>
          </li>`;
      }).join("");
    }

    const runtime = list.reduce((sum, track) => sum + (Number(track.runtime) || 0), 0);
    const bpms = list.map((track) => Number(track.intel?.bpm)).filter(Number.isFinite);
    const voiceCounts = list.reduce((counts, track) => {
      const status = voiceStatus(track);
      counts[status] = (counts[status] || 0) + 1;
      return counts;
    }, {});
    refs.setRuntime.textContent = list.length ? `${fmt(runtime)} / ${flags} TRANSITION FLAGS` : "0:00 / EMPTY";
    refs.metricTracks.textContent = String(list.length);
    refs.metricBpm.textContent = bpms.length ? `${Math.round(Math.min(...bpms))}–${Math.round(Math.max(...bpms))}` : "—";
    refs.metricVoice.textContent = list.length
      ? `${voiceCounts["lyrics-detected"] || 0}L/${voiceCounts["likely-instrumental"] || 0}I`
      : "—";
    refs.metricFlags.textContent = String(flags);
    refs.mobileSetCount.textContent = String(list.length);
    refs.energyArc.innerHTML = list.map((track) => {
      const energy = Number(track.intel?.energy);
      const transition = transitions.get(track.id);
      return `<span class="energy-bar ${Number.isFinite(energy) ? "" : "unknown"} ${transition.flagged ? "flagged" : ""}" style="height:${Number.isFinite(energy) ? 10 + energy * 42 : 12}px" title="${escapeHtml(track.title)} / ENERGY ${Number.isFinite(energy) ? Math.round(energy * 100) : "—"}"></span>`;
    }).join("");
    refs.playSet.disabled = !list.length;
    refs.clearSet.disabled = !list.length;
    refs.exportSet.disabled = !list.length;
    refs.undo.disabled = !state.history.length;
    refs.context.textContent = `${state.playContext === "set" ? "SET" : "RESULTS"} / ${list.length} KEPT / ${flags} FLAGS`;
  }

  function renderControls() {
    document.querySelectorAll("[data-mode]").forEach((button) => {
      const active = button.dataset.mode === state.mode;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    refs.search.placeholder = MODE_PLACEHOLDERS[state.mode];
    if (refs.search.value !== state.query) refs.search.value = state.query;
    refs.albumFilter.value = state.album;
    refs.genreFilter.value = state.genre;
    refs.vocalFilter.value = state.vocal;
    refs.themeFilter.value = state.theme;
    refs.bpmMin.value = state.bpmMin;
    refs.bpmMax.value = state.bpmMax;
    refs.sort.value = state.sort;
  }

  function currentTrack() {
    return trackById.get(state.currentId) || null;
  }

  function activeQueue() {
    const ids = state.playContext === "set" ? state.setIds : state.resultQueueIds;
    return ids.map((id) => trackById.get(id)).filter(Boolean);
  }

  function renderPlayer() {
    const track = currentTrack();
    if (!track) {
      refs.playerState.textContent = "READY";
      refs.title.textContent = "ANY-TIME LAB";
      refs.meta.textContent = "SEARCH / AUDITION / BUILD";
      refs.art.hidden = true;
      refs.addCurrent.disabled = true;
      refs.inspectCurrent.disabled = true;
      refs.play.disabled = true;
      return;
    }
    const queue = activeQueue();
    const index = queue.findIndex((item) => item.id === track.id);
    refs.playerState.textContent = refs.audio.src ? (refs.audio.paused ? "PAUSED" : "PLAYING") : "READY";
    refs.title.textContent = track.title;
    refs.meta.textContent = `${trackMeta(track)} / ${index >= 0 ? `${index + 1}/${queue.length}` : "OUTSIDE QUEUE"}`;
    refs.art.src = assetPath(track.art);
    refs.art.alt = `${track.title} artwork`;
    refs.art.hidden = !track.art;
    refs.artLink.href = assetPath(track.page) || "./any-time.html";
    refs.addCurrent.disabled = state.setIds.includes(track.id);
    refs.inspectCurrent.disabled = false;
    refs.play.disabled = false;
    refs.play.textContent = !refs.audio.paused && refs.audio.src ? "Ⅱ PAUSE" : "▶ PLAY";
    updateMediaSession(track);
  }

  function renderAll() {
    renderResults();
    renderSet();
    renderPlayer();
  }

  function addToSet(id) {
    if (!trackById.has(id) || state.setIds.includes(id)) {
      announce("Already in set");
      return;
    }
    pushHistory();
    state.setIds.push(id);
    saveState();
    renderAll();
    announce(`${trackById.get(id).title} added`);
  }

  function removeFromSet(id) {
    if (!state.setIds.includes(id)) return;
    pushHistory();
    state.setIds = state.setIds.filter((trackId) => trackId !== id);
    saveState();
    renderAll();
    announce(`${trackById.get(id)?.title || "Track"} removed`);
  }

  function moveSetTrack(id, delta) {
    const index = state.setIds.indexOf(id);
    const target = index + delta;
    if (index < 0 || target < 0 || target >= state.setIds.length) return;
    pushHistory();
    const next = state.setIds.slice();
    const [moved] = next.splice(index, 1);
    next.splice(target, 0, moved);
    state.setIds = next;
    saveState();
    renderAll();
    announce(`Moved to ${target + 1}`);
  }

  function moveBefore(sourceId, targetId) {
    if (!sourceId || !targetId || sourceId === targetId) return;
    const next = state.setIds.filter((id) => id !== sourceId);
    const index = next.indexOf(targetId);
    if (index < 0) return;
    pushHistory();
    next.splice(index, 0, sourceId);
    state.setIds = next;
    movingId = "";
    saveState();
    renderAll();
    announce(`Moved before ${trackById.get(targetId)?.title || "track"}`);
  }

  function undoSet() {
    const snapshot = state.history.pop();
    if (!snapshot) return;
    state.setIds = snapshot;
    saveState();
    renderAll();
    announce("Set edit undone");
  }

  function loadTrack(id, context, autoplay = true) {
    const track = trackById.get(id);
    if (!track?.audio) {
      announce("Audio unavailable");
      return;
    }
    state.currentId = id;
    state.playContext = context === "set" ? "set" : "results";
    attemptedFallback = false;
    refs.audio.src = encodeURI(assetPath(track.audio));
    refs.audio.load();
    refs.seek.value = "0";
    refs.seek.disabled = true;
    refs.elapsed.textContent = "0:00";
    refs.duration.textContent = track.runtime ? fmt(track.runtime) : "--:--";
    saveState();
    renderAll();
    if (autoplay) refs.audio.play().catch(() => announce("Press play to start"));
  }

  function togglePlay() {
    const track = currentTrack();
    if (!track) {
      const first = state.setIds[0] || state.resultQueueIds[0];
      if (first) loadTrack(first, state.setIds.length ? "set" : "results", true);
      return;
    }
    if (!refs.audio.src) loadTrack(track.id, state.playContext, true);
    else if (refs.audio.paused) refs.audio.play().catch(() => announce("Press play to start"));
    else refs.audio.pause();
  }

  function stepTrack(direction, fromEnded = false) {
    const queue = activeQueue();
    if (!queue.length) return;
    const index = Math.max(0, queue.findIndex((track) => track.id === state.currentId));
    if (direction < 0 && refs.audio.currentTime > 3) {
      refs.audio.currentTime = 0;
      return;
    }
    const candidate = queue[index + direction];
    if (candidate) loadTrack(candidate.id, state.playContext, true);
    else if (!fromEnded) loadTrack(queue[direction > 0 ? 0 : queue.length - 1].id, state.playContext, true);
    else announce("Queue complete");
  }

  function playWholeSet() {
    if (!state.setIds.length) return;
    loadTrack(state.setIds[0], "set", true);
    setMobilePanel("set");
  }

  function updateProgress() {
    const duration = Number.isFinite(refs.audio.duration) ? refs.audio.duration : currentTrack()?.runtime;
    const progress = Number.isFinite(duration) && duration > 0 ? refs.audio.currentTime / duration : 0;
    refs.elapsed.textContent = fmt(refs.audio.currentTime);
    refs.duration.textContent = fmt(duration);
    refs.seek.disabled = !Number.isFinite(duration);
    refs.seek.value = String(Math.round(Math.max(0, Math.min(1, progress)) * 1000));
  }

  function addMetric(label, value) {
    const wrapper = document.createElement("div");
    const term = document.createElement("dt");
    const description = document.createElement("dd");
    term.textContent = label;
    description.textContent = value;
    wrapper.append(term, description);
    refs.detailMetrics.append(wrapper);
  }

  function evidenceFor(track) {
    const evaluated = evaluateTrack(track);
    const reasons = evaluated?.reasons || [];
    if (track.albumSignal) reasons.push(`ALBUM SIGNAL: ${track.albumSignal}`);
    if (track.genres.length) reasons.push(`GENRE SIGNALS: ${track.genres.join(" / ")}`);
    if (track.intel?.themes?.length) {
      reasons.push(`CURATED THEMES: ${track.intel.themes.map((id) => themeById.get(id)?.title || id).join(" / ")}`);
    }
    return [...new Set(reasons)];
  }

  function relatedTo(track) {
    const baseTokens = new Set(tokens(`${track.albumSignal} ${track.genres.join(" ")} ${track.intel?.vibes?.join(" ") || ""}`));
    return tracks
      .filter((candidate) => candidate.id !== track.id)
      .map((candidate) => {
        const candidateTokens = new Set(tokens(`${candidate.albumSignal} ${candidate.genres.join(" ")} ${candidate.intel?.vibes?.join(" ") || ""}`));
        let score = [...baseTokens].filter((token) => candidateTokens.has(token)).length;
        if (track.albumKey === candidate.albumKey) score += 1.2;
        if (track.intel?.themes?.some((id) => candidate.intel?.themes?.includes(id))) score += 5;
        const first = Number(track.intel?.bpm);
        const second = Number(candidate.intel?.bpm);
        if (Number.isFinite(first) && Number.isFinite(second)) score += Math.max(0, 2 - Math.abs(first - second) / 12);
        return { candidate, score };
      })
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score || a.candidate.libraryIndex - b.candidate.libraryIndex)
      .slice(0, 6)
      .map((item) => item.candidate);
  }

  function openDetail(id) {
    const track = trackById.get(id);
    if (!track) return;
    detailTrackId = id;
    refs.detailArt.src = assetPath(track.art);
    refs.detailArt.alt = `${track.title} artwork`;
    refs.detailState.textContent = track.intel ? "ANALYZED / MACHINE REVIEW" : "TITLE + ALBUM SIGNAL ONLY";
    refs.detailTitle.textContent = track.title;
    refs.detailAlbum.textContent = `${track.albumLabel} / ${track.albumSignal || "NO ALBUM SIGNAL"}`;
    refs.detailSource.href = assetPath(track.page);
    refs.detailPlay.dataset.track = id;
    refs.detailAdd.dataset.track = id;
    refs.detailAdd.disabled = false;
    refs.detailAdd.textContent = state.setIds.includes(id) ? "− CUT" : "+ ADD";
    refs.detailMetrics.replaceChildren();
    addMetric("BPM", shortNumber(track.intel?.bpm));
    addMetric("ENERGY", Number.isFinite(track.intel?.energy) ? Math.round(track.intel.energy * 100) : "—");
    addMetric("DRAMA", Number.isFinite(track.intel?.drama) ? Math.round(track.intel.drama * 100) : "—");
    addMetric("VOICE", voiceShort(track));
    addMetric("KEY EST.", track.intel?.key ? `${track.intel.key} ${track.intel.mode || ""}` : "—");
    const evidence = evidenceFor(track);
    refs.detailEvidence.innerHTML = evidence.length
      ? evidence.map((item) => `<span>${escapeHtml(item)}</span>`).join("")
      : `<span>TITLE INDEXED</span>`;
    refs.detailConfidence.textContent = track.intel
      ? `BPM ${Math.round((track.intel.tempoConfidence || 0) * 100)}% / VOICE ${Math.round((track.intel.voice?.confidence || 0) * 100)}%`
      : "NO ACOUSTIC ANALYSIS";
    if (track.intel?.segments?.length) {
      refs.transcriptState.textContent = `${String(track.intel.voice.language || "unknown").toUpperCase()} / MACHINE DRAFT / REVIEW`;
      refs.transcriptCopy.textContent = track.intel.segments.map((segment) => `[${fmt(segment.start)}] ${segment.text}`).join("\n\n");
    } else {
      refs.transcriptState.textContent = voiceStatus(track) === "likely-instrumental" ? "LIKELY INSTRUMENTAL / REVIEW" : "NOT INDEXED";
      refs.transcriptCopy.textContent = voiceStatus(track) === "likely-instrumental"
        ? "No credible lyrical transcript was found in the analyzed scans. Confirm by ear."
        : "No transcript is indexed for this track.";
    }
    refs.relatedTracks.innerHTML = relatedTo(track).map((candidate) => `
      <div class="related-item" data-track="${escapeHtml(candidate.id)}">
        <span>${escapeHtml(candidate.title)} / ${escapeHtml(candidate.albumLabel)} / ${shortNumber(candidate.intel?.bpm)} BPM</span>
        <button type="button" data-action="related-add" ${state.setIds.includes(candidate.id) ? "disabled" : ""}>${state.setIds.includes(candidate.id) ? "IN SET" : "+ ADD"}</button>
      </div>`).join("");
    if (!refs.detail.open) refs.detail.showModal();
  }

  function exportSet() {
    const list = setTracks();
    const payload = {
      title: "Any-Time Lab Set",
      exportedAt: new Date().toISOString(),
      count: list.length,
      runtimeSeconds: list.reduce((sum, track) => sum + (Number(track.runtime) || 0), 0),
      tracks: list.map((track, index) => ({
        position: index + 1,
        title: track.title,
        album: track.albumLabel,
        bpm: track.intel?.bpm || null,
        energy: track.intel?.energy || null,
        voiceStatus: voiceStatus(track),
        transition: transitionBetween(index ? list[index - 1] : null, track).note,
        page: track.page,
        audio: track.audio
      }))
    };
    const blob = new Blob([`${JSON.stringify(payload, null, 2)}\n`], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "any-time-lab-set.json";
    link.click();
    window.setTimeout(() => URL.revokeObjectURL(link.href), 0);
    announce("Set exported");
  }

  function setMobilePanel(panel) {
    state.mobilePanel = panel;
    document.querySelectorAll("[data-mobile-panel]").forEach((button) => {
      const active = button.dataset.mobilePanel === panel;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    document.querySelectorAll("[data-panel]").forEach((column) => {
      column.classList.toggle("mobile-active", column.dataset.panel === panel);
    });
    saveState();
  }

  function resetFilters() {
    state.query = "";
    state.album = "";
    state.genre = "";
    state.vocal = "";
    state.theme = "";
    state.bpmMin = "";
    state.bpmMax = "";
    state.sort = "relevance";
    refreshResults(true);
    announce("Filters reset");
  }

  function updateMediaSession(track) {
    if (!("mediaSession" in navigator) || !("MediaMetadata" in window)) return;
    navigator.mediaSession.metadata = new MediaMetadata({
      title: track.title,
      artist: track.albumLabel,
      album: "Any-Time Lab",
      artwork: track.art ? [{ src: new URL(assetPath(track.art), window.location.href).href }] : []
    });
  }

  refs.albumFilter.innerHTML += albums.map((album) => `<option value="${escapeHtml(album.key)}">${escapeHtml(album.label)} / ${album.tracks.length}</option>`).join("");
  refs.genreFilter.innerHTML += allGenres.map((genre) => `<option value="${escapeHtml(genre)}">${escapeHtml(genre)}</option>`).join("");
  refs.themeFilter.innerHTML += intelligence.themes.map((theme) => `<option value="${escapeHtml(theme.id)}">${escapeHtml(theme.title)}</option>`).join("");
  refs.coverage.textContent = `INDEX ${intelligence.coverage.libraryTracks.toLocaleString()} / BPM ${intelligence.coverage.analyzedTracks} / WORDS ${intelligence.coverage.transcriptTracks}`;
  refs.coverage.title = intelligence.caveats.join(" ");
  refs.coverageReadout.textContent = `TITLE ${intelligence.coverage.libraryTracks.toLocaleString()} / BPM ${intelligence.coverage.analyzedTracks} / WORDS ${intelligence.coverage.transcriptTracks}`;

  document.querySelectorAll("[data-mode]").forEach((button) => {
    button.addEventListener("click", () => {
      state.mode = button.dataset.mode;
      state.resultLimit = RESULT_STEP;
      refreshResults(true);
      refs.search.focus();
      announce(`${MODE_LABELS[state.mode]} active`);
    });
  });

  refs.search.addEventListener("input", () => {
    state.query = refs.search.value;
    refreshResults(true);
  });
  refs.clearSearch.addEventListener("click", () => {
    state.query = "";
    refs.search.value = "";
    refreshResults(true);
    refs.search.focus();
  });
  refs.albumFilter.addEventListener("change", () => { state.album = refs.albumFilter.value; refreshResults(true); });
  refs.genreFilter.addEventListener("change", () => { state.genre = refs.genreFilter.value; refreshResults(true); });
  refs.vocalFilter.addEventListener("change", () => { state.vocal = refs.vocalFilter.value; refreshResults(true); });
  refs.themeFilter.addEventListener("change", () => { state.theme = refs.themeFilter.value; refreshResults(true); });
  refs.bpmMin.addEventListener("input", () => { state.bpmMin = refs.bpmMin.value; refreshResults(true); });
  refs.bpmMax.addEventListener("input", () => { state.bpmMax = refs.bpmMax.value; refreshResults(true); });
  refs.sort.addEventListener("change", () => { state.sort = refs.sort.value; refreshResults(true); });
  refs.resetFilters.addEventListener("click", resetFilters);
  refs.coverage.addEventListener("click", () => announce(intelligence.caveats[0], 4200));
  refs.loadMore.addEventListener("click", () => { state.resultLimit += RESULT_STEP; renderResults(); });

  refs.results.addEventListener("click", (event) => {
    const card = event.target.closest("[data-track]");
    const id = card?.dataset.track;
    if (!id) return;
    const action = event.target.closest("[data-action]")?.dataset.action;
    if (action === "play") loadTrack(id, "results", true);
    if (action === "add") addToSet(id);
    if (action === "detail") openDetail(id);
  });

  refs.setList.addEventListener("click", (event) => {
    const card = event.target.closest("[data-track]");
    const id = card?.dataset.track;
    if (!id) return;
    const action = event.target.closest("[data-action]")?.dataset.action;
    if (action === "play") loadTrack(id, "set", true);
    if (action === "detail") openDetail(id);
    if (action === "up") moveSetTrack(id, -1);
    if (action === "down") moveSetTrack(id, 1);
    if (action === "cut") removeFromSet(id);
    if (action === "move") {
      if (!movingId) {
        movingId = id;
        renderSet();
        announce(`Moving ${trackById.get(id).title}; choose a position`);
      } else if (movingId === id) {
        movingId = "";
        renderSet();
        announce("Move cancelled");
      } else {
        moveBefore(movingId, id);
      }
    }
  });
  refs.setList.addEventListener("dragstart", (event) => {
    const card = event.target.closest(".set-card");
    if (!card?.dataset.track) return;
    draggedId = card.dataset.track;
    card.classList.add("dragging");
    event.dataTransfer.effectAllowed = "move";
    event.dataTransfer.setData("text/plain", draggedId);
  });
  refs.setList.addEventListener("dragover", (event) => {
    const card = event.target.closest(".set-card");
    if (!draggedId || !card?.dataset.track || card.dataset.track === draggedId) return;
    event.preventDefault();
    card.classList.add("drop-ready");
  });
  refs.setList.addEventListener("dragleave", (event) => event.target.closest(".set-card")?.classList.remove("drop-ready"));
  refs.setList.addEventListener("drop", (event) => {
    const card = event.target.closest(".set-card");
    if (!card?.dataset.track) return;
    event.preventDefault();
    moveBefore(draggedId || event.dataTransfer.getData("text/plain"), card.dataset.track);
    draggedId = "";
  });
  refs.setList.addEventListener("dragend", () => {
    draggedId = "";
    document.querySelectorAll(".dragging, .drop-ready").forEach((card) => card.classList.remove("dragging", "drop-ready"));
  });

  refs.addCurrent.addEventListener("click", () => { if (state.currentId) addToSet(state.currentId); });
  refs.undo.addEventListener("click", undoSet);
  refs.inspectCurrent.addEventListener("click", () => { if (state.currentId) openDetail(state.currentId); });
  refs.play.addEventListener("click", togglePlay);
  refs.previous.addEventListener("click", () => stepTrack(-1));
  refs.next.addEventListener("click", () => stepTrack(1));
  refs.playSet.addEventListener("click", playWholeSet);
  refs.clearSet.addEventListener("click", () => {
    if (!state.setIds.length || !window.confirm("Clear the current set? You can undo this once.")) return;
    pushHistory();
    state.setIds = [];
    saveState();
    renderAll();
    announce("Set cleared");
  });
  refs.exportSet.addEventListener("click", exportSet);

  refs.detailClose.addEventListener("click", () => refs.detail.close());
  refs.detail.addEventListener("click", (event) => { if (event.target === refs.detail) refs.detail.close(); });
  refs.detailPlay.addEventListener("click", () => { if (detailTrackId) loadTrack(detailTrackId, "results", true); });
  refs.detailAdd.addEventListener("click", () => {
    if (!detailTrackId) return;
    if (state.setIds.includes(detailTrackId)) removeFromSet(detailTrackId);
    else addToSet(detailTrackId);
    openDetail(detailTrackId);
  });
  refs.relatedTracks.addEventListener("click", (event) => {
    const row = event.target.closest("[data-track]");
    if (row && event.target.closest("[data-action='related-add']")) {
      addToSet(row.dataset.track);
      openDetail(detailTrackId);
    }
  });

  document.querySelectorAll("[data-mobile-panel]").forEach((button) => {
    button.addEventListener("click", () => setMobilePanel(button.dataset.mobilePanel));
  });

  refs.seek.addEventListener("pointerdown", () => { isScrubbing = true; });
  refs.seek.addEventListener("input", () => {
    const duration = refs.audio.duration;
    if (Number.isFinite(duration)) {
      const time = (Number(refs.seek.value) / 1000) * duration;
      refs.elapsed.textContent = fmt(time);
      refs.audio.currentTime = time;
    }
  });
  refs.seek.addEventListener("change", () => { isScrubbing = false; updateProgress(); });

  refs.audio.addEventListener("play", renderAll);
  refs.audio.addEventListener("pause", renderAll);
  refs.audio.addEventListener("timeupdate", () => { if (!isScrubbing) updateProgress(); });
  refs.audio.addEventListener("durationchange", updateProgress);
  refs.audio.addEventListener("ended", () => stepTrack(1, true));
  refs.audio.addEventListener("error", () => {
    const track = currentTrack();
    if (!attemptedFallback && track?.sourceAudio && track.sourceAudio !== track.audio) {
      attemptedFallback = true;
      refs.audio.src = encodeURI(assetPath(track.sourceAudio));
      refs.audio.load();
      refs.audio.play().catch(() => announce("Audio fallback ready"));
    } else {
      announce("Media error");
    }
  });

  document.addEventListener("keydown", (event) => {
    const target = event.target;
    if (target instanceof HTMLInputElement || target instanceof HTMLSelectElement || target instanceof HTMLButtonElement || target instanceof HTMLTextAreaElement) return;
    if (event.code === "Space") { event.preventDefault(); togglePlay(); }
    if (event.code === "ArrowRight") stepTrack(1);
    if (event.code === "ArrowLeft") stepTrack(-1);
  });

  if ("mediaSession" in navigator) {
    const handlers = {
      play: () => refs.audio.play().catch(() => announce("Press play to start")),
      pause: () => refs.audio.pause(),
      previoustrack: () => stepTrack(-1),
      nexttrack: () => stepTrack(1)
    };
    Object.entries(handlers).forEach(([action, handler]) => {
      try { navigator.mediaSession.setActionHandler(action, handler); } catch { /* Unsupported action. */ }
    });
  }

  renderControls();
  refreshResults(true);
  renderSet();
  renderPlayer();
  setMobilePanel(state.mobilePanel);
  announce("Ready");
})();
