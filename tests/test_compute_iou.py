import pytest
from src.evaluate import compute_iou
from src.models import MinimalSource


@pytest.mark.parametrize("r_start, r_end, g_start, g_end, expected", [
    (0, 100, 0, 100, 1.0),
    (0, 100, 200, 300, 0.0),
    (0, 100, 50, 150, 1/3),
    (0, 100, 100, 200, 0.0),
    (0, 100, 25, 75, 0.5),
    (25, 75, 0, 100, 0.5),
    (0, 100, 0, 200, 0.5),
    (0, 100, 50, 100, 0.5),
    (50, 150, 0, 100, 1/3)
])


def test_iou(r_start, r_end, g_start, g_end, expected):
    r = MinimalSource(file_path="example.py", first_character_index=r_start, last_character_index=r_end)
    g = MinimalSource(file_path="example.py", first_character_index=g_start, last_character_index=g_end)

    assert compute_iou(r, g) == expected
