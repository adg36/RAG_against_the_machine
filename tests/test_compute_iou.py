import pytest
from src.models import MinimalSource


def compute_iou(retrieved_source: MinimalSource, ground_truth: MinimalSource) -> float:

    r_start = retrieved_source.first_character_index
    r_end = retrieved_source.last_character_index
    g_start = ground_truth.first_character_index
    g_end = ground_truth.last_character_index

    begin_intersection = max(r_start, g_start)
    end_intersection = min(r_end, g_end)
    intersection = end_intersection - begin_intersection
    if intersection < 0:
        intersection = 0

    union = ((r_end - r_start) + (g_end - g_start)) - intersection

    return intersection / union if union > 0 else 0.0


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
