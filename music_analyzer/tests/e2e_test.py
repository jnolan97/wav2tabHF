from pathlib import Path
from app.main import process_audio

def test_dummy(tmp_path):
    sample = Path(__file__).parent / "sample.mp3"
    if not sample.exists():
        return  # no sample in repo
    process_audio(sample, tmp_path)
    assert (tmp_path / "output_tab.gp5").exists()