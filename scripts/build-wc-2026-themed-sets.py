#!/usr/bin/env python3
"""Discover transcript themes and build finite, evidence-backed DJ set proposals."""

from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ROOT = Path(__file__).resolve().parents[1]
MIX_DIR = ROOT / "WC-2026-FINAL-MIX"
ANALYSIS_PATH = MIX_DIR / "analysis" / "analysis-manifest.json"
SETS_DIR = MIX_DIR / "sets"

FILLER_WORDS = {
    "ain", "baby", "cause", "come", "coming", "da", "day", "did", "does",
    "don", "gonna", "got", "hey", "just", "know", "la", "let", "like",
    "ll", "make", "man", "na", "need", "oh", "ooh", "right", "say", "says",
    "thing", "things", "time", "ve", "wanna", "way", "yeah", "youre",
}

THEMES = (
    {
        "id": "systems-under-pressure",
        "label": "SYSTEMS / PRESSURE",
        "title": "Systems Under Pressure",
        "thesis": "Human signals pushing through platforms, contracts, labor systems, and digital enclosure.",
        "energyTarget": 0.64,
        "terms": (
            "system data digital silicon signal platform process prompt engine service terms conditions "
            "transaction invoice bandwidth convenience labor work money contract network machine power "
            "maintenance infrastructure control surveillance repair friction"
        ),
        "seeds": (
            "Digital Middlemen",
            "The Terms and Conditions of Living",
            "The Transactional Truth",
            "Fingerprints in the Silicon",
            "Kiosk Republics",
            "Steel & Static — The 2 AM Express",
        ),
    },
    {
        "id": "home-is-a-signal",
        "label": "HOME / REPAIR",
        "title": "Home Is a Signal",
        "thesis": "Domestic labor, kinship, grief, devotion, and repair moving from private rooms toward collective release.",
        "energyTarget": 0.52,
        "terms": (
            "home house room kitchen table family mother father child hands repair laundry basket domestic "
            "prayer devotion grief memory care healing water light alive enough country hunger love body "
            "tender living sanctuary breaking"
        ),
        "seeds": (
            "Sanctuary After the Breaking",
            "Appliance Prayer",
            "Visible Repair",
            "Homebound Loop",
            "Kitchen Prep at Dawn",
            "Water Light Finale",
        ),
    },
    {
        "id": "borderless-cypher",
        "label": "BORDERLESS CYPHER",
        "title": "Borderless Cypher",
        "thesis": "Ancestral rhythm, migration, language, and neighborhood movement crossing the Andes, Atlantic, and city blocks.",
        "energyTarget": 0.61,
        "terms": (
            "ancestral ancestor cypher rhythm resistance migration border barrio favela passinho kuduro andes "
            "altiplano bronx bamako mali tamani diaspora sangre zinc radio roots blade fire warrior "
            "stadium pulse flow voltage street concrete"
        ),
        "seeds": (
            "The Cypher of the Andes",
            "Favela Footwork Circuit (1)",
            "Lisbon Kuduro Voltage",
            "Passinho das Quadras",
            "Malian Pulse",
            "GPU Azmari Flow",
        ),
    },
    {
        "id": "pressure-to-release",
        "label": "PRESSURE / RELEASE",
        "title": "Pressure to Release",
        "thesis": "A late-room arc from compressed tension through impact, survival, and a controlled cathartic landing.",
        "energyTarget": 0.70,
        "terms": (
            "pressure tension panic abyss fire ignition steel static edge survival struggle blood dust concrete "
            "power crown king ransom purgatory catharsis release water light alive victory banner fractured "
            "gate night shadow resistance force"
        ),
        "seeds": (
            "Abyssal Transmission",
            "King Don’t Beg the Gate",
            "Chemical Ignition",
            "Arquitectura Anti-Gris",
            "Port-Out Ransom",
            "Survival Taxonomy",
        ),
    },
)


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def transcript_text(track: dict[str, Any]) -> str:
    relative = track.get("voice", {}).get("transcriptPath")
    if not relative:
        return ""
    path = MIX_DIR / relative.removeprefix("./")
    if not path.exists():
        return ""
    payload = load_json(path)
    segments = payload.get("segments") or []
    credible = [segment.get("text", "") for segment in segments if segment.get("text")]
    return " ".join(credible) or payload.get("text", "")


def corpus_for(tracks: list[dict[str, Any]]) -> list[str]:
    documents = []
    for track in tracks:
        transcript = transcript_text(track)
        title_context = f"{track['title']} {track['title']} {track['album']}"
        documents.append(f"{title_context} {transcript}".strip())
    return documents


def discover_topics(
    matrix: Any,
    vectorizer: TfidfVectorizer,
    tracks: list[dict[str, Any]],
    count: int = 7,
) -> tuple[list[dict[str, Any]], np.ndarray]:
    model = NMF(n_components=count, init="nndsvda", random_state=26, max_iter=800)
    weights = model.fit_transform(matrix)
    terms = np.asarray(vectorizer.get_feature_names_out())
    topics = []
    for index, component in enumerate(model.components_):
        top_terms = terms[np.argsort(component)[::-1][:12]].tolist()
        top_track_indexes = np.argsort(weights[:, index])[::-1][:8]
        topics.append({
            "id": f"topic-{index + 1}",
            "topTerms": top_terms,
            "topTracks": [
                {
                    "id": tracks[item]["id"],
                    "title": tracks[item]["title"],
                    "weight": round(float(weights[item, index]), 4),
                }
                for item in top_track_indexes
            ],
        })
    return topics, weights


def resolve_seed_indexes(tracks: list[dict[str, Any]], seed_titles: tuple[str, ...]) -> list[int]:
    by_title = {normalize(track["title"]): index for index, track in enumerate(tracks)}
    missing = [title for title in seed_titles if normalize(title) not in by_title]
    if missing:
        raise ValueError(f"Unknown theme seed titles: {', '.join(missing)}")
    return [by_title[normalize(title)] for title in seed_titles]


def choose_theme_members(
    theme: dict[str, Any],
    tracks: list[dict[str, Any]],
    matrix: Any,
    vectorizer: TfidfVectorizer,
    topic_weights: np.ndarray,
    set_size: int = 18,
) -> tuple[list[int], list[dict[str, Any]], dict[int, dict[str, Any]]]:
    query = vectorizer.transform([theme["terms"]])
    lexical = cosine_similarity(matrix, query).ravel()
    seed_indexes = resolve_seed_indexes(tracks, theme["seeds"])
    selected = list(seed_indexes)
    album_counts = Counter(tracks[index]["album"] for index in selected)
    rounds = [{"round": 0, "method": "editorial seeds", "trackIds": [tracks[index]["id"] for index in selected]}]
    evidence: dict[int, dict[str, Any]] = {
        index: {"samplingRound": 0, "lexicalSimilarity": float(lexical[index]), "neighborSimilarity": 1.0}
        for index in selected
    }

    additions_per_round = math.ceil((set_size - len(selected)) / 2)
    for round_number in (1, 2):
        centroid = np.asarray(matrix[selected].mean(axis=0))
        neighbors = cosine_similarity(matrix, centroid).ravel()
        topic_centroid = topic_weights[selected].mean(axis=0)
        topic_norm = np.linalg.norm(topic_centroid) or 1.0
        topic_similarity = (topic_weights @ topic_centroid) / (
            np.linalg.norm(topic_weights, axis=1) * topic_norm + 1e-9
        )
        target = theme["energyTarget"]
        candidates = []
        for index, track in enumerate(tracks):
            if index in selected:
                continue
            energy = track.get("editorial", {}).get("energyScore", 0.5)
            acoustic_fit = 1.0 - min(1.0, abs(energy - target))
            title_words = set(normalize(f"{track['title']} {track['album']}").split())
            theme_words = set(normalize(theme["terms"]).split())
            title_hits = len(title_words & theme_words)
            if track["voice"]["status"] == "lyrics-detected" and lexical[index] == 0 and title_hits == 0:
                continue
            score = (
                0.45 * lexical[index]
                + 0.30 * neighbors[index]
                + 0.12 * topic_similarity[index]
                + 0.08 * acoustic_fit
                + min(0.12, title_hits * 0.04)
                - max(0, album_counts[track["album"]] - 1) * 0.07
            )
            candidates.append((float(score), index, float(neighbors[index]), title_hits))
        candidates.sort(reverse=True)
        additions = []
        needed = min(additions_per_round, set_size - len(selected))
        for score, index, neighbor_score, title_hits in candidates:
            album = tracks[index]["album"]
            if album_counts[album] >= 3:
                continue
            selected.append(index)
            additions.append(index)
            album_counts[album] += 1
            evidence[index] = {
                "samplingRound": round_number,
                "lexicalSimilarity": float(lexical[index]),
                "neighborSimilarity": neighbor_score,
                "selectionScore": score,
                "titleTermHits": title_hits,
            }
            if len(additions) == needed:
                break
        rounds.append({
            "round": round_number,
            "method": "TF-IDF seed-centroid snowball",
            "trackIds": [tracks[index]["id"] for index in additions],
        })
    return selected[:set_size], rounds, evidence


def bpm_pair(first: float, second: float) -> tuple[float, float, float]:
    first_options = [value for value in (first / 2, first, first * 2) if 72 <= value <= 180]
    second_options = [value for value in (second / 2, second, second * 2) if 72 <= value <= 180]
    candidates = [(abs(a - b), a, b) for a in first_options for b in second_options]
    delta, adjusted_first, adjusted_second = min(candidates)
    return adjusted_first, adjusted_second, delta


def energy_target(position: int, count: int) -> float:
    progress = position / max(1, count - 1)
    if progress <= 0.18:
        return 0.34 + (progress / 0.18) * 0.18
    if progress <= 0.72:
        return 0.52 + ((progress - 0.18) / 0.54) * 0.35
    if progress <= 0.86:
        return 0.87 + ((progress - 0.72) / 0.14) * 0.08
    return 0.95 - ((progress - 0.86) / 0.14) * 0.32


def transition_cost(previous: dict[str, Any], candidate: dict[str, Any]) -> float:
    previous_features = previous["features"]
    candidate_features = candidate["features"]
    _, _, tempo_delta = bpm_pair(previous_features["bpm"], candidate_features["bpm"])
    energy_delta = abs(previous["editorial"]["energyScore"] - candidate["editorial"]["energyScore"])
    same_album = 0.42 if previous["album"] == candidate["album"] else 0.0
    both_lyrics = 0.07 if previous["voice"]["status"] == candidate["voice"]["status"] == "lyrics-detected" else 0.0
    return min(1.0, tempo_delta / 30.0) * 0.62 + max(0.0, energy_delta - 0.22) * 0.8 + same_album + both_lyrics


def sequence_members(member_indexes: list[int], tracks: list[dict[str, Any]], beam_width: int = 96) -> list[int]:
    count = len(member_indexes)
    beam: list[tuple[float, tuple[int, ...]]] = [(0.0, tuple())]
    for position in range(count):
        target = energy_target(position, count)
        expanded = []
        for cost, sequence in beam:
            used = set(sequence)
            for index in member_indexes:
                if index in used:
                    continue
                track = tracks[index]
                energy = track["editorial"]["energyScore"]
                position_cost = abs(energy - target) * 1.45
                if position == 0:
                    position_cost += track["editorial"]["dramaScore"] * 0.12
                if sequence:
                    position_cost += transition_cost(tracks[sequence[-1]], track)
                expanded.append((cost + position_cost, sequence + (index,)))
        expanded.sort(key=lambda item: item[0])
        beam = expanded[:beam_width]
    return list(beam[0][1])


def matched_terms(theme: dict[str, Any], document: str, limit: int = 5) -> list[str]:
    words = set(normalize(document).split())
    terms = []
    for term in normalize(theme["terms"]).split():
        if term in words and term not in terms:
            terms.append(term)
    return terms[:limit]


def transcript_evidence(track: dict[str, Any], theme: dict[str, Any]) -> dict[str, Any] | None:
    relative = track.get("voice", {}).get("transcriptPath")
    if not relative:
        return None
    path = MIX_DIR / relative.removeprefix("./")
    if not path.exists():
        return None
    payload = load_json(path)
    terms = set(normalize(theme["terms"]).split())
    segments = [segment for segment in payload.get("segments", []) if segment.get("text")]
    selected = next(
        (segment for segment in segments if set(normalize(segment["text"]).split()) & terms),
        segments[0] if segments else None,
    )
    if selected is None:
        return None
    excerpt = re.sub(r"\s+", " ", selected["text"]).strip()
    return {
        "path": relative,
        "startSeconds": round(float(selected.get("start", 0)), 2),
        "excerpt": excerpt[:240],
        "machineDraft": True,
    }


def transition_record(previous: dict[str, Any] | None, track: dict[str, Any]) -> dict[str, Any] | None:
    if previous is None:
        return None
    first, second, delta = bpm_pair(previous["features"]["bpm"], track["features"]["bpm"])
    energy_delta = track["editorial"]["energyScore"] - previous["editorial"]["energyScore"]
    if abs(energy_delta) < 0.04:
        movement = "energy holds"
    elif energy_delta > 0:
        movement = f"energy rises {round(energy_delta * 100)}"
    else:
        movement = f"energy releases {round(abs(energy_delta) * 100)}"
    first_confidence = previous["features"].get("keyConfidence", 0)
    second_confidence = track["features"].get("keyConfidence", 0)
    harmonic = "key estimate is advisory"
    if min(first_confidence, second_confidence) >= 0.45:
        harmonic = f"review {previous['features']['keyEstimate']} to {track['features']['keyEstimate']}"
    return {
        "fromId": previous["id"],
        "adjustedBpmFrom": round(first, 1),
        "adjustedBpmTo": round(second, 1),
        "bpmDelta": round(delta, 1),
        "energyDelta": round(energy_delta, 3),
        "note": f"{round(first)} to {round(second)} BPM; {movement}; {harmonic}.",
    }


def build_theme_record(
    theme: dict[str, Any],
    tracks: list[dict[str, Any]],
    documents: list[str],
    matrix: Any,
    vectorizer: TfidfVectorizer,
    topic_weights: np.ndarray,
) -> dict[str, Any]:
    members, rounds, evidence = choose_theme_members(theme, tracks, matrix, vectorizer, topic_weights)
    sequence = sequence_members(members, tracks)
    records = []
    previous = None
    for position, index in enumerate(sequence, start=1):
        track = tracks[index]
        voice = track["voice"]
        item_evidence = evidence[index]
        records.append({
            "position": position,
            "id": track["id"],
            "index": track["index"],
            "title": track["title"],
            "album": track["album"],
            "durationSeconds": track["features"]["durationSeconds"],
            "bpm": track["features"]["bpm"],
            "energyScore": track["editorial"]["energyScore"],
            "dramaScore": track["editorial"]["dramaScore"],
            "voiceStatus": voice["status"],
            "transcriptConfidence": voice.get("confidence", 0),
            "reviewRequired": voice.get("reviewRequired", True),
            "samplingRound": item_evidence["samplingRound"],
            "evidence": {
                "matchedTerms": matched_terms(theme, documents[index]),
                "lexicalSimilarity": round(item_evidence.get("lexicalSimilarity", 0), 4),
                "neighborSimilarity": round(item_evidence.get("neighborSimilarity", 0), 4),
                "basis": "editorial seed" if item_evidence["samplingRound"] == 0 else "snowball neighbor",
                "transcript": transcript_evidence(track, theme),
            },
            "transitionFromPrevious": transition_record(previous, track),
        })
        previous = track
    duration = sum(item["durationSeconds"] for item in records)
    return {
        "id": theme["id"],
        "label": theme["label"],
        "title": theme["title"],
        "thesis": theme["thesis"],
        "status": "editorial proposal / listening review required",
        "durationSeconds": round(duration, 2),
        "trackCount": len(records),
        "voiceCounts": dict(Counter(item["voiceStatus"] for item in records)),
        "seedTrackIds": rounds[0]["trackIds"],
        "samplingRounds": rounds,
        "order": [item["id"] for item in records],
        "tracks": records,
    }


def markdown_report(payload: dict[str, Any]) -> str:
    lines = [
        "# WC 2026 Themed DJ Set Proposals",
        "",
        "These are finite editorial proposals, not automatic truth. Transcript drafts, language labels, BPM, and key estimates require listening review before performance.",
        "",
        "## Discovery pass",
        "",
        "The builder uses title-weighted transcript TF-IDF, seven NMF topic neighborhoods, two rounds of seed-centroid snowball sampling, then a separate transition/energy sequencing pass.",
        "",
    ]
    for topic in payload["topicDiscovery"]:
        titles = ", ".join(track["title"] for track in topic["topTracks"][:4])
        lines.append(f"- **{topic['id']}**: {', '.join(topic['topTerms'][:8])}. Nearest tracks: {titles}.")
    for theme in payload["themes"]:
        minutes = theme["durationSeconds"] / 60
        lines.extend([
            "",
            f"## {theme['title']}",
            "",
            theme["thesis"],
            "",
            f"**{theme['trackCount']} tracks / {minutes:.1f} minutes / {theme['status']}**",
            "",
            "| # | Track | Album | Voice | BPM | Energy | Entry / transition |",
            "|---:|---|---|---|---:|---:|---|",
        ])
        for item in theme["tracks"]:
            transition = item["transitionFromPrevious"]
            note = "Opening bed" if transition is None else transition["note"]
            lines.append(
                f"| {item['position']} | {item['title']} | {item['album']} | {item['voiceStatus']} | "
                f"{item['bpm']:.1f} | {item['energyScore']:.2f} | {note} |"
            )
        review_titles = [item["title"] for item in theme["tracks"] if item["reviewRequired"]]
        lines.extend([
            "",
            "**Review queue:** " + (", ".join(review_titles) if review_titles else "No machine flags."),
        ])
    lines.extend([
        "",
        "## Performance rule",
        "",
        "The selected order is a transition hypothesis. Confirm phrasing, intro/outro room, explicit language, gain, and the half/double-time interpretation in headphones before treating any set as performance-ready.",
        "",
    ])
    return "\n".join(lines)


def transcript_review_report(payload: dict[str, Any]) -> str:
    lines = [
        "# WC 2026 Iterative Transcript Theme Review",
        "",
        "This document is a machine-assisted review surface. Excerpts are draft transcription evidence, not approved lyrics. Read them while listening and correct the source transcript JSON before changing a theme decision.",
        "",
        "## Review protocol",
        "",
        "1. Confirm whether the track is lyrical, sampled speech, or instrumental.",
        "2. Correct the cited transcript segment and language before interpreting it.",
        "3. Accept or reject the seed/neighbor relationship.",
        "4. Audition the proposed predecessor and annotate usable mix-in/mix-out points.",
        "",
    ]
    for theme in payload["themes"]:
        lines.extend([f"## {theme['title']}", "", theme["thesis"], ""])
        for item in theme["tracks"]:
            evidence = item["evidence"]
            terms = ", ".join(evidence["matchedTerms"]) or "no direct term; inspect neighbor relation"
            transcript = evidence["transcript"]
            status = f"{item['voiceStatus']} / {round(item['transcriptConfidence'] * 100)}%"
            lines.append(
                f"### {item['position']:02d}. {item['title']} — {evidence['basis']} (round {item['samplingRound']})"
            )
            lines.append("")
            lines.append(f"- **Evidence:** {terms}; lexical {evidence['lexicalSimilarity']:.3f}; neighbor {evidence['neighborSimilarity']:.3f}.")
            lines.append(f"- **Voice draft:** {status}.")
            if transcript:
                lines.append(
                    f"- **Draft excerpt [{transcript['startSeconds']:.1f}s]:** “{transcript['excerpt']}”"
                )
                lines.append(f"- **Source:** `{transcript['path']}`")
            else:
                lines.append("- **Draft excerpt:** no full transcript; verify the instrumental/sample classification by ear.")
            lines.append("")
    return "\n".join(lines)


def validate(payload: dict[str, Any], all_ids: set[str]) -> None:
    assert len(payload["themes"]) == len(THEMES)
    for theme in payload["themes"]:
        order = theme["order"]
        assert len(order) == theme["trackCount"] == 18
        assert len(set(order)) == len(order)
        assert set(order) <= all_ids
        assert [item["id"] for item in theme["tracks"]] == order
        assert theme["tracks"][0]["transitionFromPrevious"] is None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-topics", action="store_true", help="Print discovered topic neighborhoods.")
    args = parser.parse_args()

    analysis = load_json(ANALYSIS_PATH)
    tracks = analysis["tracks"]
    documents = corpus_for(tracks)
    stop_words = sorted(set(ENGLISH_STOP_WORDS) | FILLER_WORDS)
    vectorizer = TfidfVectorizer(
        stop_words=stop_words,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.88,
        max_features=6500,
        sublinear_tf=True,
        strip_accents="unicode",
        token_pattern=r"(?u)\b[^\W\d_][^\W_]+\b",
    )
    matrix = vectorizer.fit_transform(documents)
    topics, topic_weights = discover_topics(matrix, vectorizer, tracks)
    themes = [
        build_theme_record(theme, tracks, documents, matrix, vectorizer, topic_weights)
        for theme in THEMES
    ]
    payload = {
        "version": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceAnalysisGeneratedAt": analysis.get("generatedAt"),
        "status": "editorial proposals / human listening review required",
        "method": {
            "discovery": "title-weighted transcript TF-IDF plus 7-topic NMF",
            "sampling": "6 editorial seeds followed by 2 seed-centroid snowball rounds",
            "sequencing": "beam search over energy arc, half/double-time BPM distance, album spacing, and vocal density",
            "keyUse": "advisory only when both key estimates have at least 45% confidence",
        },
        "topicDiscovery": topics,
        "themes": themes,
    }
    validate(payload, {track["id"] for track in tracks})

    SETS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = SETS_DIR / "themed-sets.json"
    js_path = MIX_DIR / "themed-sets.js"
    report_path = SETS_DIR / "themed-sets.md"
    transcript_review_path = SETS_DIR / "transcript-theme-review.md"
    json_text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    json_path.write_text(json_text, encoding="utf-8")
    js_path.write_text(f"window.WC_2026_THEMED_SETS = {json_text.rstrip()};\n", encoding="utf-8")
    report_path.write_text(markdown_report(payload), encoding="utf-8")
    transcript_review_path.write_text(transcript_review_report(payload), encoding="utf-8")

    if args.print_topics:
        for topic in topics:
            titles = ", ".join(track["title"] for track in topic["topTracks"][:5])
            print(f"{topic['id']}: {', '.join(topic['topTerms'])}")
            print(f"  {titles}")
    for theme in themes:
        print(f"{theme['title']}: {theme['trackCount']} tracks / {theme['durationSeconds'] / 60:.1f} minutes")


if __name__ == "__main__":
    main()
