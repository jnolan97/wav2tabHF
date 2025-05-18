import argparse
from pathlib import Path
from . import separation, transcription, tempo, tab_generation

SUPPORTED_EXT = {".mp3", ".wav", ".flac"}

def _process_file(f: Path, outdir: Path):
    print("=================", f.name, "=================")
    stems = separation.separate_stems(f, outdir)
    bpm = tempo.detect_bpm(f)
    ts = tempo.estimate_time_signature(f)
    guitar_notes = transcription.transcribe(stems["guitar"], "guitar")
    bass_notes = transcription.transcribe(stems["bass"], "bass")
    tab_generation.write_gp5(guitar_notes, bass_notes, bpm, ts, outdir / (f.stem + "_tab.gp5"))


def main():
    ap = argparse.ArgumentParser(description="Audio Tab Generator")
    ap.add_argument("--input", required=True, type=Path, help="File or directory with audio")
    ap.add_argument("--output", required=True, type=Path, help="Output directory")
    args = ap.parse_args()

    inp, out = args.input.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    files = [inp] if inp.is_file() else [p for p in inp.iterdir() if p.suffix.lower() in SUPPORTED_EXT]
    if not files:
        print("No audio files found."); return
    for f in files:
        _process_file(f, out)
    print("All done ✨. Results in", out)

if __name__ == "__main__":
    main()
