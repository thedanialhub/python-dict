from dictionary import dictionary

def test_pronunciation_field():
    for entry in dictionary:
        assert "pronunciation" in entry
        assert isinstance(entry["pronunciation"], str)