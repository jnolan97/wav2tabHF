import argparse
from pathlib import Path

from . import tempo
from .. import separation, transcription, tab_generation


def process_audio(audio_path: Path, output_dir: Path):
    stems = separation.separate_stems(audio_path, output_dir)

    bpm = tempo.detect_bpm(audio_path)
    ts = tempo.estimate_time_signature(audio_path)
    print(f"[Tempo] BPM ≈ {bpm}")
    print(f"[Tempo] Time Signature ≈ {ts}")

    guitar_notes = transcription.transcribe(stems["guitar"], "guitar")
    bass_notes = transcription.transcribe(stems["bass"], "bass")

    tab_path = output_dir / "output_tab.gp5"
    tab_generation.write_gp5(guitar_notes, bass_notes, bpm, ts, tab_path)

    print("=== Finished ===")
    print(f"Guitar stem: {stems['guitar']}")
    print(f"Bass stem  : {stems['bass']}")
    print(f"Vocals stem: {stems['vocals']}")
    print(f"Tab file   : {tab_path}")


def main():
    parser = argparse.ArgumentParser(description="Audio → Stems + Tabs")
    parser.add_argument("--input", required=True, type=Path, help="Audio file path")
    parser.add_argument("--output", required=True, type=Path, help="Output directory")
    args = parser.parse_args()

    process_audio(args.input, args.output)


if __name__ == "__main__":
    main()