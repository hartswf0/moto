#!/usr/bin/env python3
"""Measure, transcribe, and editorially classify the WC 2026 mix."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import math
import os
import re
import signal
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
MIX_DIR = ROOT / "WC-2026-FINAL-MIX"
MANIFEST_PATH = MIX_DIR / "mix-manifest.js"
ANALYSIS_DIR = MIX_DIR / "analysis"
FEATURE_DIR = ANALYSIS_DIR / "features"
SCAN_DIR = ANALYSIS_DIR / "scans"
TRANSCRIPT_DIR = ANALYSIS_DIR / "transcripts"
OUTPUT_JSON = ANALYSIS_DIR / "analysis-manifest.json"
OUTPUT_JS = MIX_DIR / "analysis-manifest.js"
ANALYSIS_VERSION = 1
SAMPLE_RATE = 22050
HOP_LENGTH = 512

NUMBA_CACHE_DIR = Path(os.environ.get("TMPDIR", "/tmp")) / "moto-audio-numba-cache"
NUMBA_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("NUMBA_CACHE_DIR", str(NUMBA_CACHE_DIR))

MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
KEY_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("features", "scan", "full", "all", "compile"), default="all")
    parser.add_argument("--model", default="base", help="Cached Whisper model name")
    parser.add_argument("--workers", type=int, default=max(1, min(4, (os.cpu_count() or 4) // 2)))
    parser.add_argument("--track", action="append", type=int, help="Mix index to process; repeat as needed")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def load_manifest() -> dict[str, Any]:
    source = MANIFEST_PATH.read_text(encoding="utf-8")
    try:
        payload = source.split("=", 1)[1].strip().rstrip(";")
        return json.loads(payload)
    except (IndexError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Cannot parse {MANIFEST_PATH}: {error}") from error


def track_slug(track: dict[str, Any]) -> str:
    name = Path(track["artwork"]).stem
    return name[:-7] if name.endswith("-ticket") else name


def audio_path(track: dict[str, Any]) -> Path:
    return (MIX_DIR / track["audio"]).resolve()


def cache_path(folder: Path, track: dict[str, Any]) -> Path:
    return folder / f"{track_slug(track)}.json"


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(f"{path.suffix}.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def finite(value: Any, fallback: float = 0.0) -> float:
    try:
        number = float(np.asarray(value).reshape(-1)[0])
    except (TypeError, ValueError, IndexError):
        return fallback
    return number if math.isfinite(number) else fallback


def rounded(value: Any, digits: int = 3) -> float:
    return round(finite(value), digits)


def key_estimate(chroma: np.ndarray) -> tuple[str, str, float]:
    vector = np.mean(chroma, axis=1)
    if not np.any(vector):
        return "unknown", "unknown", 0.0
    scores: list[tuple[float, int, str]] = []
    for root in range(12):
        for mode, profile in (("major", MAJOR_PROFILE), ("minor", MINOR_PROFILE)):
            score = finite(np.corrcoef(vector, np.roll(profile, root))[0, 1], -1.0)
            scores.append((score, root, mode))
    scores.sort(reverse=True)
    best, second = scores[0], scores[1]
    confidence = np.clip((best[0] - second[0]) / 0.35, 0.0, 1.0)
    return KEY_NAMES[best[1]], best[2], finite(confidence)


def measure_track(track: dict[str, Any]) -> dict[str, Any]:
    import librosa

    path = audio_path(track)
    if not path.exists():
        raise FileNotFoundError(path)
    y, sr = librosa.load(path, sr=SAMPLE_RATE, mono=True, res_type="soxr_hq")
    duration = len(y) / sr
    if duration <= 0:
        raise RuntimeError(f"Empty audio: {path}")

    stft = np.abs(librosa.stft(y, n_fft=2048, hop_length=HOP_LENGTH))
    power = stft**2
    rms = librosa.feature.rms(S=stft, frame_length=2048, hop_length=HOP_LENGTH)[0]
    rms_db = 20 * np.log10(np.maximum(rms, 1e-9))
    onset = librosa.onset.onset_strength(S=librosa.amplitude_to_db(stft, ref=np.max), sr=sr, hop_length=HOP_LENGTH)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset, sr=sr, hop_length=HOP_LENGTH)
    beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=HOP_LENGTH)
    beat_intervals = np.diff(beat_times)
    beat_cv = finite(np.std(beat_intervals) / np.mean(beat_intervals), 1.0) if len(beat_intervals) else 1.0
    beat_stability = float(np.clip(1.0 - beat_cv, 0.0, 1.0))
    pulse_salience = finite(np.median(onset[beats]) / max(np.percentile(onset, 90), 1e-9), 0.0) if len(beats) else 0.0
    tempo_confidence = 0.55 * beat_stability + 0.45 * min(pulse_salience, 1.0)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset, sr=sr, hop_length=HOP_LENGTH, backtrack=False)
    onset_rate = len(onset_frames) / max(duration / 60, 1e-6)

    frequencies = librosa.fft_frequencies(sr=sr, n_fft=2048)
    low_end_ratio = finite(np.sum(power[frequencies < 250]) / max(np.sum(power), 1e-12))
    centroid = librosa.feature.spectral_centroid(S=stft, sr=sr)[0]
    rolloff = librosa.feature.spectral_rolloff(S=stft, sr=sr, roll_percent=0.85)[0]
    chroma = librosa.feature.chroma_stft(S=stft, sr=sr, hop_length=HOP_LENGTH)
    key, mode, key_confidence = key_estimate(chroma)

    contour: list[float] = []
    for frames in np.array_split(rms_db, 8):
        contour.append(rounded(np.mean(frames), 2) if len(frames) else -90.0)
    start_db = finite(np.mean(contour[:2]), -90.0)
    end_db = finite(np.mean(contour[-2:]), -90.0)
    peak_position = int(np.argmax(contour)) + 1
    total_rms = math.sqrt(finite(np.mean(y**2), 0.0))
    crest_db = 20 * math.log10(max(finite(np.max(np.abs(y))), 1e-9) / max(total_rms, 1e-9))

    return {
        "index": track["index"],
        "id": track["songPage"],
        "slug": track_slug(track),
        "durationSeconds": rounded(duration, 2),
        "bpm": rounded(tempo, 1),
        "halfTimeBpm": rounded(tempo / 2, 1),
        "doubleTimeBpm": rounded(tempo * 2, 1),
        "tempoConfidence": rounded(tempo_confidence, 3),
        "onsetsPerMinute": rounded(onset_rate, 1),
        "rmsDb": rounded(np.mean(rms_db), 2),
        "dynamicRangeDb": rounded(np.percentile(rms_db, 90) - np.percentile(rms_db, 20), 2),
        "crestDb": rounded(crest_db, 2),
        "brightnessHz": rounded(np.median(centroid), 1),
        "rolloffHz": rounded(np.median(rolloff), 1),
        "lowEndRatio": rounded(low_end_ratio, 4),
        "keyEstimate": key,
        "modeEstimate": mode,
        "keyConfidence": rounded(key_confidence, 3),
        "energyContourDb": contour,
        "energyRiseDb": rounded(end_db - start_db, 2),
        "energyPeakEighth": peak_position,
    }


def run_features(tracks: list[dict[str, Any]], workers: int, force: bool) -> None:
    pending = [track for track in tracks if force or not cache_path(FEATURE_DIR, track).exists()]
    if not pending:
        print("Acoustic features already cached.", flush=True)
        return
    print(f"Measuring {len(pending)} tracks with {workers} workers.", flush=True)
    if workers == 1:
        for completed, track in enumerate(pending, start=1):
            result = measure_track(track)
            write_json(cache_path(FEATURE_DIR, track), result)
            print(f"FEATURE {completed:03d}/{len(pending):03d}  {track['title']}", flush=True)
        return
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        jobs = {executor.submit(measure_track, track): track for track in pending}
        completed = 0
        for future in concurrent.futures.as_completed(jobs):
            track = jobs[future]
            result = future.result()
            write_json(cache_path(FEATURE_DIR, track), result)
            completed += 1
            print(f"FEATURE {completed:03d}/{len(pending):03d}  {track['title']}", flush=True)


def scan_ranges(duration: float, window: float = 18.0) -> list[tuple[float, float]]:
    if duration <= window * 2:
        return [(0.0, duration)]
    available = max(0.0, duration - window)
    starts = [available * point for point in (0.08, 0.32, 0.56, 0.80)]
    ranges: list[tuple[float, float]] = []
    for start in starts:
        end = min(duration, start + window)
        if not ranges or start > ranges[-1][1] + 1:
            ranges.append((start, end))
        else:
            ranges[-1] = (ranges[-1][0], end)
    return ranges


def compact_segment(segment: dict[str, Any]) -> dict[str, Any]:
    words = [
        {
            "word": word.get("word", ""),
            "start": rounded(word.get("start"), 2),
            "end": rounded(word.get("end"), 2),
            "probability": rounded(word.get("probability"), 3),
        }
        for word in segment.get("words", [])
    ]
    if not words and str(segment.get("text", "")).strip():
        probability = float(np.clip(math.exp(finite(segment.get("avg_logprob"), -2.0)), 0.0, 1.0))
        words = [
            {
                "word": token,
                "start": rounded(segment.get("start"), 2),
                "end": rounded(segment.get("end"), 2),
                "probability": rounded(probability, 3),
            }
            for token in re.findall(r"\S+", str(segment.get("text", "")))
        ]
    return {
        "start": rounded(segment.get("start"), 2),
        "end": rounded(segment.get("end"), 2),
        "text": str(segment.get("text", "")).strip(),
        "avgLogprob": rounded(segment.get("avg_logprob"), 3),
        "compressionRatio": rounded(segment.get("compression_ratio"), 3),
        "noSpeechProbability": rounded(segment.get("no_speech_prob"), 3),
        "words": words,
    }


def transcription_evidence(segments: list[dict[str, Any]], duration: float, scanned: float) -> dict[str, Any]:
    credible_segments = [
        segment for segment in segments
        if segment["avgLogprob"] >= -1.1
        and segment["compressionRatio"] <= 2.6
        and segment["noSpeechProbability"] <= 0.75
        and segment["text"]
    ]
    words = [word for segment in credible_segments for word in segment["words"] if re.search(r"\w", word["word"], re.UNICODE)]
    credible_words = [word for word in words if word["probability"] >= 0.35]
    average_probability = finite(np.mean([word["probability"] for word in words]), 0.0) if words else 0.0
    vocal_seconds = sum(max(0.0, segment["end"] - segment["start"]) for segment in credible_segments)
    scan_coverage = min(1.0, scanned / max(duration, 1e-6))

    if len(credible_words) >= 12 and average_probability >= 0.38:
        status = "lyrics-detected"
        confidence = np.clip(0.42 + average_probability * 0.48 + min(len(credible_words), 80) / 800, 0.0, 0.96)
    elif len(credible_words) >= 3:
        status = "vocal-fragment"
        confidence = np.clip(0.35 + average_probability * 0.42, 0.0, 0.78)
    else:
        status = "likely-instrumental"
        confidence = np.clip(0.46 + scan_coverage * 0.24 - average_probability * 0.12, 0.0, 0.72)

    return {
        "status": status,
        "confidence": rounded(confidence, 3),
        "wordCount": len(words),
        "credibleWordCount": len(credible_words),
        "segmentCount": len(credible_segments),
        "averageWordProbability": rounded(average_probability, 3),
        "vocalSeconds": rounded(vocal_seconds, 2),
        "scanCoverage": rounded(scan_coverage, 3),
        "reviewRequired": bool(status != "lyrics-detected" or confidence < 0.72 or average_probability < 0.70),
    }


def transcribe_track(model: Any, track: dict[str, Any], scope: str) -> dict[str, Any]:
    feature = json.loads(cache_path(FEATURE_DIR, track).read_text(encoding="utf-8"))
    duration = finite(feature["durationSeconds"])
    ranges = scan_ranges(duration) if scope == "scan" else [(0.0, duration)]
    timed_out_ranges: list[list[float]] = []

    if scope == "full":
        import whisper

        scan = json.loads(cache_path(SCAN_DIR, track).read_text(encoding="utf-8"))
        language = scan.get("language") or None
        audio = whisper.load_audio(str(audio_path(track)))
        chunk_seconds = 45.0
        chunk_samples = int(chunk_seconds * whisper.audio.SAMPLE_RATE)
        segments = []
        text_parts = []

        def timeout_handler(_signum: int, _frame: Any) -> None:
            raise TimeoutError("Whisper chunk exceeded 75 seconds")

        previous_handler = signal.signal(signal.SIGALRM, timeout_handler)
        try:
            for offset in range(0, len(audio), chunk_samples):
                start = offset / whisper.audio.SAMPLE_RATE
                end = min(duration, (offset + chunk_samples) / whisper.audio.SAMPLE_RATE)
                signal.setitimer(signal.ITIMER_REAL, 75.0)
                try:
                    chunk_result = model.transcribe(
                        audio[offset : offset + chunk_samples],
                        task="transcribe",
                        language=language,
                        verbose=None,
                        fp16=False,
                        temperature=0,
                        beam_size=2,
                        condition_on_previous_text=False,
                        word_timestamps=False,
                    )
                except TimeoutError:
                    timed_out_ranges.append([rounded(start, 2), rounded(end, 2)])
                    continue
                finally:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                text_parts.append(str(chunk_result.get("text", "")).strip())
                for raw_segment in chunk_result.get("segments", []):
                    segment = compact_segment(raw_segment)
                    segment["start"] = rounded(segment["start"] + start, 2)
                    segment["end"] = rounded(segment["end"] + start, 2)
                    for word in segment["words"]:
                        word["start"] = rounded(word["start"] + start, 2)
                        word["end"] = rounded(word["end"] + start, 2)
                    segments.append(segment)
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous_handler)
        result = {"language": language or "unknown", "text": " ".join(part for part in text_parts if part)}
        scanned = duration - sum(end - start for start, end in timed_out_ranges)
    else:
        clips = ",".join(f"{start:.2f},{end:.2f}" for start, end in ranges)
        result = model.transcribe(
            str(audio_path(track)),
            task="transcribe",
            language=None,
            verbose=None,
            fp16=False,
            temperature=0,
            beam_size=2,
            condition_on_previous_text=False,
            word_timestamps=True,
            hallucination_silence_threshold=2.0,
            clip_timestamps=clips,
        )
        segments = [compact_segment(segment) for segment in result.get("segments", [])]
        scanned = sum(end - start for start, end in ranges)

    evidence = transcription_evidence(segments, duration, scanned)
    if timed_out_ranges:
        evidence["reviewRequired"] = True
    return {
        "analysisVersion": ANALYSIS_VERSION,
        "index": track["index"],
        "id": track["songPage"],
        "slug": track_slug(track),
        "model": model.dims.n_audio_state,
        "modelName": "base",
        "scope": scope,
        "language": result.get("language", "unknown"),
        "text": str(result.get("text", "")).strip(),
        "sampledRanges": [[rounded(start, 2), rounded(end, 2)] for start, end in ranges],
        "timedOutRanges": timed_out_ranges,
        "segments": segments,
        "evidence": evidence,
    }


def load_whisper_model(model_name: str) -> Any:
    try:
        import whisper
    except ImportError as error:
        raise RuntimeError("Install openai-whisper before transcription.") from error
    print(f"Loading cached Whisper model: {model_name}", flush=True)
    return whisper.load_model(model_name, device="cpu", download_root=str(Path.home() / ".cache" / "whisper"))


def run_transcription(tracks: list[dict[str, Any]], model_name: str, scope: str, force: bool) -> None:
    for track in tracks:
        if not cache_path(FEATURE_DIR, track).exists():
            raise RuntimeError(f"Feature cache missing for track {track['index']}; run --mode features first.")
    if scope == "scan":
        pending = [track for track in tracks if force or not cache_path(SCAN_DIR, track).exists()]
    else:
        candidates = []
        for track in tracks:
            scan_file = cache_path(SCAN_DIR, track)
            if not scan_file.exists():
                raise RuntimeError(f"Scan cache missing for track {track['index']}; run --mode scan first.")
            scan = json.loads(scan_file.read_text(encoding="utf-8"))
            if scan["evidence"]["credibleWordCount"] >= 3:
                candidates.append(track)
        pending = [track for track in candidates if force or not cache_path(TRANSCRIPT_DIR, track).exists()]
        print(f"{len(candidates)} tracks have evidence requiring full transcription.", flush=True)
    if not pending:
        print(f"Whisper {scope} results already cached.", flush=True)
        return

    model = load_whisper_model(model_name)
    for index, track in enumerate(pending, start=1):
        print(f"{scope.upper()} {index:03d}/{len(pending):03d}  {track['title']}", flush=True)
        result = transcribe_track(model, track, scope)
        result["modelName"] = model_name
        target = cache_path(SCAN_DIR if scope == "scan" else TRANSCRIPT_DIR, track)
        write_json(target, result)


def rank_map(values: list[float]) -> list[float]:
    if len(values) < 2:
        return [0.5 for _ in values]
    order = np.argsort(np.argsort(np.asarray(values, dtype=float), kind="stable"), kind="stable")
    return [finite(rank / (len(values) - 1)) for rank in order]


def editorialize(records: list[dict[str, Any]]) -> None:
    available = [record for record in records if record.get("features")]
    if not available:
        return
    fields = {
        "tempo": rank_map([record["features"]["bpm"] for record in available]),
        "onsets": rank_map([record["features"]["onsetsPerMinute"] for record in available]),
        "loudness": rank_map([record["features"]["rmsDb"] for record in available]),
        "dynamics": rank_map([record["features"]["dynamicRangeDb"] for record in available]),
        "brightness": rank_map([record["features"]["brightnessHz"] for record in available]),
        "lowEnd": rank_map([record["features"]["lowEndRatio"] for record in available]),
    }
    for index, record in enumerate(available):
        feature = record["features"]
        pace = 0.48 * fields["tempo"][index] + 0.34 * fields["onsets"][index] + 0.18 * feature["tempoConfidence"]
        energy = 0.68 * fields["loudness"][index] + 0.22 * fields["onsets"][index] + 0.10 * fields["lowEnd"][index]
        tonal_tension = 0.75 if feature["modeEstimate"] == "minor" and feature["keyConfidence"] >= 0.25 else 0.35
        drama = 0.42 * energy + 0.30 * fields["dynamics"][index] + 0.16 * tonal_tension + 0.12 * pace
        pace = finite(np.clip(pace, 0.0, 1.0))
        energy = finite(np.clip(energy, 0.0, 1.0))
        drama = finite(np.clip(drama, 0.0, 1.0))

        tone = "balanced"
        if fields["brightness"][index] <= 0.28:
            tone = "dark"
        elif fields["brightness"][index] >= 0.72:
            tone = "bright"
        if feature["modeEstimate"] == "minor" and feature["keyConfidence"] >= 0.35:
            tone += " / tense"
        elif feature["modeEstimate"] == "major" and feature["keyConfidence"] >= 0.35:
            tone += " / open"

        vibes = []
        vibes.append("driving" if pace >= 0.68 else "measured" if pace <= 0.32 else "moving")
        vibes.append("forceful" if energy >= 0.68 else "restrained" if energy <= 0.32 else "grounded")
        if fields["dynamics"][index] >= 0.70:
            vibes.append("volatile")
        elif fields["dynamics"][index] <= 0.30:
            vibes.append("steady")
        if fields["brightness"][index] >= 0.75:
            vibes.append("bright")
        elif fields["brightness"][index] <= 0.25:
            vibes.append("shadowed")

        record["editorial"] = {
            "paceScore": rounded(pace, 3),
            "energyScore": rounded(energy, 3),
            "dramaScore": rounded(drama, 3),
            "tone": tone,
            "vibes": vibes,
            "dramaticRole": "bridge",
        }

    drama_ranks = rank_map([record["editorial"]["dramaScore"] for record in available])
    for index, record in enumerate(available):
        editorial = record["editorial"]
        feature = record["features"]
        if drama_ranks[index] >= 0.82:
            role = "peak"
        elif feature["energyRiseDb"] >= 2.0 and drama_ranks[index] >= 0.42:
            role = "build"
        elif editorial["paceScore"] <= 0.34 and editorial["energyScore"] <= 0.36:
            role = "release"
        elif editorial["paceScore"] <= 0.40 and drama_ranks[index] >= 0.48:
            role = "suspense"
        else:
            role = "bridge"
        editorial["dramaticRole"] = role


def target_arc(position: int, count: int) -> tuple[float, float]:
    point = position / max(count - 1, 1)
    if point < 0.18:
        local = point / 0.18
        return 0.20 + 0.25 * local, 0.18 + 0.27 * local
    if point < 0.58:
        local = (point - 0.18) / 0.40
        return 0.45 + 0.40 * local, 0.45 + 0.35 * local
    if point < 0.78:
        local = (point - 0.58) / 0.20
        return 0.85 + 0.12 * local, 0.80 + 0.15 * local
    local = (point - 0.78) / 0.22
    return 0.90 - 0.68 * local, 0.78 - 0.60 * local


def assign_suggested_order(records: list[dict[str, Any]]) -> list[str]:
    candidates = [record for record in records if record.get("editorial")]
    remaining = candidates[:]
    sequence: list[dict[str, Any]] = []
    for position in range(len(candidates)):
        target_drama, target_pace = target_arc(position, len(candidates))
        previous = sequence[-1] if sequence else None

        def cost(record: dict[str, Any]) -> tuple[float, int]:
            editorial = record["editorial"]
            value = abs(editorial["dramaScore"] - target_drama)
            value += 0.55 * abs(editorial["paceScore"] - target_pace)
            if previous:
                if record["albumKey"] == previous["albumKey"]:
                    value += 0.24
                previous_bpm = max(previous["features"]["bpm"], 1)
                current_bpm = max(record["features"]["bpm"], 1)
                tempo_distance = abs(math.log2(current_bpm / previous_bpm))
                tempo_distance = min(tempo_distance, abs(tempo_distance - 1), abs(tempo_distance + 1))
                value += min(tempo_distance, 0.5) * 0.20
            return value, record["index"]

        chosen = min(remaining, key=cost)
        remaining.remove(chosen)
        sequence.append(chosen)
    for rank, record in enumerate(sequence, start=1):
        record["editorial"]["suggestedRank"] = rank
    return [record["id"] for record in sequence]


def compile_analysis(manifest: dict[str, Any]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for track in manifest["tracks"]:
        feature_file = cache_path(FEATURE_DIR, track)
        scan_file = cache_path(SCAN_DIR, track)
        transcript_file = cache_path(TRANSCRIPT_DIR, track)
        feature = json.loads(feature_file.read_text(encoding="utf-8")) if feature_file.exists() else None
        scan = json.loads(scan_file.read_text(encoding="utf-8")) if scan_file.exists() else None
        transcript = json.loads(transcript_file.read_text(encoding="utf-8")) if transcript_file.exists() else None
        evidence_source = transcript or scan
        voice = {
            "status": "unprocessed",
            "confidence": 0,
            "reviewRequired": True,
            "transcriptPath": None,
        }
        if evidence_source:
            voice = {
                **evidence_source["evidence"],
                "language": evidence_source.get("language", "unknown"),
                "scope": evidence_source.get("scope", "scan"),
                "transcriptPath": f"./analysis/transcripts/{track_slug(track)}.json" if transcript else None,
            }
            voice["reviewRequired"] = bool(
                voice["status"] != "lyrics-detected"
                or voice["confidence"] < 0.72
                or voice.get("averageWordProbability", 0) < 0.70
            )
        records.append({
            "id": track["songPage"],
            "index": track["index"],
            "title": track["title"],
            "album": track["album"],
            "albumKey": track["albumKey"],
            "features": feature,
            "voice": voice,
        })

    editorialize(records)
    suggested_order = assign_suggested_order(records)
    counts: dict[str, int] = {}
    for record in records:
        status = record["voice"]["status"]
        counts[status] = counts.get(status, 0) + 1
    payload = {
        "analysisVersion": ANALYSIS_VERSION,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "method": {
            "features": "librosa 0.11 full-track relative analysis",
            "transcription": "Whisper base multilingual with distributed scans and confidence filtering",
            "classification": "Corpus-relative heuristics; machine estimates require editorial review",
        },
        "trackCount": len(records),
        "analyzedCount": sum(1 for record in records if record["features"]),
        "voiceCounts": counts,
        "suggestedOrder": suggested_order,
        "tracks": records,
    }
    write_json(OUTPUT_JSON, payload)
    OUTPUT_JS.write_text(
        "window.WC_2026_AUDIO_ANALYSIS = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Compiled {payload['analyzedCount']}/{payload['trackCount']} analyzed tracks.", flush=True)
    print(f"Voice evidence: {counts}", flush=True)
    return payload


def main() -> int:
    args = parse_args()
    manifest = load_manifest()
    tracks = manifest["tracks"]
    if args.track:
        selected = [track for track in tracks if track["index"] in set(args.track)]
        missing = sorted(set(args.track) - {track["index"] for track in selected})
        if missing:
            raise RuntimeError(f"Unknown mix indexes: {missing}")
    else:
        selected = tracks[: args.limit or None]

    for folder in (FEATURE_DIR, SCAN_DIR, TRANSCRIPT_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    if args.mode in ("features", "all"):
        run_features(selected, max(1, args.workers), args.force)
    if args.mode in ("scan", "all"):
        run_transcription(selected, args.model, "scan", args.force)
    if args.mode in ("full", "all"):
        run_transcription(selected, args.model, "full", args.force)
    compile_analysis(manifest)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted; completed caches are preserved.", file=sys.stderr)
        raise SystemExit(130)
