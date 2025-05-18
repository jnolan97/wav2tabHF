from app.tab_generation import _pitch_to_string_fret, STANDARD_GUITAR_TUNING

def test_mapping_low_e():
    string_idx, fret = _pitch_to_string_fret(40, STANDARD_GUITAR_TUNING)  # E2
    assert string_idx == 5 and fret == 0
