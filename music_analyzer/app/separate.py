from pathlib import Path
import subprocess
import shutil

HTDEMUCS_MODEL = "htdemucs_6s"  # 6‑stem model incl. guitar & bass


def separate_stems(audio_path: Path, output_dir: Path) -> dict:
    """Run Demucs and return dict of paths for each requested stem."""
    audio_path = Path(audio_path).expanduser().resolve()
    output_dir = Path(output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[Demucs] Separating {audio_path.name} …")
    cmd = [
        "demucs",
        "-n", HTDEMUCS_MODEL,
        "--two-stems", "none",  # keep all six stems
        str(audio_path),
        "-o", str(output_dir),
    ]
    subprocess.run(cmd, check=True)

    # Demucs writes to output_dir/trackname/stem.wav ; move wanted stems up
    track_folder = output_dir / audio_path.stem
    stems_map = {
        "guitar": track_folder / "guitar.wav",
        "bass": track_folder / "bass.wav",
        "vocals": track_folder / "vocals.wav",
    }
    for name, src in stems_map.items():
        if not src.exists():
            raise FileNotFoundError(f"Stem {name} not produced by Demucs")
        dst = output_dir / f"{name}.wav"
        shutil.move(src, dst)
        stems_map[name] = dst
    # clean leftover
    shutil.rmtree(track_folder, ignore_errors=True)
    print("[Demucs] Separation finished.")
    return stems_map
