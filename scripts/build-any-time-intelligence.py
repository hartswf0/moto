#!/usr/bin/env python3
"""Build the optional transcript, acoustic, and theme index for Any-Time Lab."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MEDIA_PATH = ROOT / "VOLHOLLA" / "media-manifest.json"
ANALYSIS_PATH = ROOT / "WC-2026-FINAL-MIX" / "analysis" / "analysis-manifest.json"
SETS_PATH = ROOT / "WC-2026-FINAL-MIX" / "sets" / "themed-sets.json"
OUTPUT_JSON = ROOT / "VOLHOLLA" / "any-time-intelligence.json"
OUTPUT_JS = ROOT / "VOLHOLLA" / "any-time-intelligence.js"

THEME_TERMS = {
    "systems-under-pressure": (
        "system data digital silicon signal platform process prompt engine service terms conditions "
        "transaction invoice bandwidth convenience labor work money contract network machine power "
        "maintenance infrastructure control surveillance repair friction"
    ),
    "home-is-a-signal": (
        "home house room kitchen table family mother father child hands repair laundry basket domestic "
        "prayer devotion grief memory care healing water light alive enough country hunger love body "
        "tender living sanctuary breaking"
    ),
    "borderless-cypher": (
        "ancestral ancestor cypher rhythm resistance migration border barrio favela passinho kuduro andes "
        "altiplano bronx bamako mali tamani diaspora sangre zinc radio roots blade fire warrior stadium "
        "pulse flow voltage street concrete"
    ),
    "pressure-to-release": (
        "pressure tension panic abyss fire ignition steel static edge survival struggle blood dust concrete "
        "power crown king ransom purgatory catharsis release water light alive victory banner fractured "
        "gate night shadow resistance force"
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_page(value: str) -> str:
    page = str(value or "").replace("\\", "/")
    while page.startswith("../"):
        page = page[3:]
    return page.removeprefix("./").lstrip("/")


def compact_segments(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = load_json(path)
    segments = []
    for segment in payload.get("segments", []):
        text = " ".join(str(segment.get("text", "")).split())
        if not text:
            continue
        segments.append({
            "start": round(float(segment.get("start", 0)), 2),
            "end": round(float(segment.get("end", 0)), 2),
            "text": text,
        })
    return segments


def main() -> None:
    media = load_json(MEDIA_PATH)
    analysis = load_json(ANALYSIS_PATH)
    themed_sets = load_json(SETS_PATH)

    library_tracks = [
        track
        for album in media.get("albums", {}).values()
        for track in album.get("tracks", [])
        if track.get("songPage")
    ]
    library_pages = {canonical_page(track["songPage"]) for track in library_tracks}
    runtime_by_page = {
        canonical_page(track["songPage"]): round(float(track["audio"]["durationSeconds"]), 3)
        for track in library_tracks
        if isinstance((track.get("audio") or {}).get("durationSeconds"), (int, float))
        and track["audio"]["durationSeconds"] > 0
    }
    theme_memberships: dict[str, list[str]] = defaultdict(list)
    theme_definitions = []
    for theme in themed_sets.get("themes", []):
        theme_id = theme["id"]
        if theme_id not in THEME_TERMS:
            raise ValueError(f"Missing terms for theme: {theme_id}")
        theme_definitions.append({
            "id": theme_id,
            "label": theme["label"],
            "title": theme["title"],
            "thesis": theme["thesis"],
            "terms": THEME_TERMS[theme_id].split(),
            "curatedCount": theme["trackCount"],
        })
        for track_id in theme.get("order", []):
            theme_memberships[canonical_page(track_id)].append(theme_id)

    records = {}
    transcript_count = 0
    for track in analysis.get("tracks", []):
        page = canonical_page(track["id"])
        if page not in library_pages:
            raise ValueError(f"Analysis track is absent from media manifest: {page}")
        feature = track.get("features", {})
        editorial = track.get("editorial", {})
        voice = track.get("voice", {})
        transcript_relative = str(voice.get("transcriptPath", "")).removeprefix("./")
        transcript_path = ROOT / "WC-2026-FINAL-MIX" / transcript_relative if transcript_relative else Path()
        segments = compact_segments(transcript_path) if transcript_relative else []
        if segments:
            transcript_count += 1
        duration = feature.get("durationSeconds")
        if page not in runtime_by_page and isinstance(duration, (int, float)) and duration > 0:
            runtime_by_page[page] = round(float(duration), 3)
        records[page] = {
            "page": page,
            "analysisIndex": track["index"],
            "title": track["title"],
            "album": track["album"],
            "bpm": feature.get("bpm"),
            "tempoConfidence": feature.get("tempoConfidence"),
            "key": feature.get("keyEstimate"),
            "mode": feature.get("modeEstimate"),
            "keyConfidence": feature.get("keyConfidence"),
            "pace": editorial.get("paceScore"),
            "energy": editorial.get("energyScore"),
            "drama": editorial.get("dramaScore"),
            "tone": editorial.get("tone"),
            "vibes": editorial.get("vibes", []),
            "role": editorial.get("dramaticRole"),
            "voice": {
                "status": voice.get("status", "unprocessed"),
                "confidence": voice.get("confidence", 0),
                "language": voice.get("language", "unknown"),
                "reviewRequired": voice.get("reviewRequired", True),
            },
            "transcriptPath": f"WC-2026-FINAL-MIX/{transcript_relative}" if transcript_relative else "",
            "segments": segments,
            "themes": theme_memberships.get(page, []),
        }

    payload = {
        "version": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceAnalysisGeneratedAt": analysis.get("generatedAt"),
        "coverage": {
            "libraryTracks": len(library_pages),
            "analyzedTracks": len(records),
            "transcriptTracks": transcript_count,
            "runtimeTracks": len(runtime_by_page),
            "curatedThemeAppearances": sum(len(items) for items in theme_memberships.values()),
            "curatedDistinctTracks": len(theme_memberships),
        },
        "caveats": [
            "Album signals are editorial descriptors, not verified genre labels.",
            "BPM, key, voice status, and transcripts are machine-assisted estimates.",
            "Unknown fields must remain unknown in the interface.",
        ],
        "themes": theme_definitions,
        "runtimeByPage": runtime_by_page,
        "records": records,
    }

    assert payload["coverage"]["libraryTracks"] == len(library_tracks)
    assert payload["coverage"]["analyzedTracks"] == len(records)
    assert payload["coverage"]["transcriptTracks"] == transcript_count
    assert set(records).issubset(library_pages)
    assert all(record["page"] == page for page, record in records.items())

    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    OUTPUT_JSON.write_text(text + "\n", encoding="utf-8")
    OUTPUT_JS.write_text(f"window.ANY_TIME_INTELLIGENCE={text};\n", encoding="utf-8")
    print(
        f"Any-Time intelligence: {len(library_pages)} library / {len(records)} analyzed / "
        f"{transcript_count} transcript tracks."
    )


if __name__ == "__main__":
    main()
