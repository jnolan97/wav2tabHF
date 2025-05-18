from typing import List
from pathlib import Path
import pyguitarpro as gp

STANDARD_GUITAR_TUNING = [64, 59, 55, 50, 45, 40]  # E4 B3 G3 D3 A2 E2
STANDARD_BASS_TUNING = [43, 38, 33, 28]  # G2 D2 A1 E1


def _pitch_to_string_fret(pitch: int, tuning: List[int]):
    """Return (string_idx, fret) picking lowest fret possible."""
    options = []
    for idx, open_note in enumerate(tuning):
        fret = pitch - open_note
        if 0 <= fret <= 24:
            options.append((idx, fret))
    if not options:
        return None, None
    # pick lowest fret; if tie, choose lowest string index (closest to floor)
    return min(options, key=lambda x: (x[1], x[0]))


def write_gp5(guitar_notes: List[dict], bass_notes: List[dict], bpm: float, ts: str, output: Path):
    song = gp.Song()
    song.tempo = int(bpm)
    ts_num, ts_den = map(int, ts.split("/"))
    song.measureHeaders = [gp.MeasureHeader(number=1, start=0, timeSignature=gp.TimeSignature(ts_num, ts_den))]

    # Guitar track
    g_track = gp.Track(song)
    g_track.name = "Guitar"
    g_track.strings = [gp.String(i + 1, note) for i, note in enumerate(STANDARD_GUITAR_TUNING)]
    song.tracks.append(g_track)

    # Bass track
    b_track = gp.Track(song)
    b_track.name = "Bass"
    b_track.strings = [gp.String(i + 1, note) for i, note in enumerate(STANDARD_BASS_TUNING)]
    song.tracks.append(b_track)

    def _add_notes(track: gp.Track, notes: List[dict], tuning: List[int]):
        measure = gp.Measure(track, song.measureHeaders[0])
        beat = gp.Beat(measure)
        last_position = 0.0
        for ev in notes:
            # simplistic: new beat each note; duration eighth
            string_idx, fret = _pitch_to_string_fret(ev["midi"], tuning)
            if string_idx is None:
                continue
            note = gp.Note(beat)
            note.string = len(tuning) - string_idx  # gp string numbering top‑down
            note.value = fret
            beat.notes.append(note)
            measure.beats.append(beat)
        track.measures.append(measure)

    _add_notes(g_track, guitar_notes, STANDARD_GUITAR_TUNING)
    _add_notes(b_track, bass_notes, STANDARD_BASS_TUNING)

    gp.write(song, str(output))
    print(f"[Tab] Written {output}")