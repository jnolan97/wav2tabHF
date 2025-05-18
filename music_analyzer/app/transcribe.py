from typing import List, Dict
from pathlib import Path
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH


class NoteEvent(dict):
    """Typed alias for note event dictionaries."""
    # fields: onset_sec, offset_sec, midi_note, velocity
    pass


def _instrument_bounds(inst: str):
    if inst == "guitar":
        return 40, 92  # E2–G#6 (standard 6‑string)
    if inst == "bass":
        return 28, 76  # E1–E5 (5‑string upper range)
    return 20, 100  # generic


def transcribe(stem_path: Path, instrument: str) -> List[NoteEvent]:
    min_f, max_f = _instrument_bounds(instrument)
    print(f"[BasicPitch] Transcribing {instrument} …")
    model_output, midi_data, note_events = predict(
        audio=stem_path,
        midi_min=min_f,
        midi_max=max_f,
        model_path=ICASSP_2022_MODEL_PATH,
    )
    notes = [
        {
            "onset": n.start,  # seconds
            "offset": n.end,
            "midi": n.pitch,
            "velocity": n.velocity,
        }
        for n in note_events
    ]
    print(f"[BasicPitch] {instrument}: {len(notes)} notes detected.")
    return notes

