from pathlib import Path
from app.main import _process_file

def test_cli_sine(tmp_path, sine_wav):
    out = tmp_path / "res"; out.mkdir()
    _process_file(Path(sine_wav), out)
    assert any(p.suffix == ".gp5" for p in out.iterdir())

# ===============================
# tests/test_tempo.py
# ===============================
from app.tempo import detect_bpm

def test_bpm_detect(sine_wav):
    bpm = detect_bpm(sine_wav)
    assert bpm > 0