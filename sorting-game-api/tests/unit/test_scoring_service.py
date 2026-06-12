from types import SimpleNamespace
from app.services.scoring_service import calculate_score, counters_dict


def test_score_zero_attempts_branch():
    assert calculate_score(0, 0, 0, 0) == 0


def test_score_all_correct_branch():
    assert calculate_score(2, 0, 3, 0) == 125


def test_score_mixed_correct_and_incorrect_branch():
    assert calculate_score(2, 1, 1, 1) == 75


def test_counters_dict_maps_game_fields():
    game = SimpleNamespace(
        insertion_correct=1,
        insertion_incorrect=2,
        bubble_correct=3,
        bubble_incorrect=4,
    )
    assert counters_dict(game) == {
        "insertion_correct": 1,
        "insertion_incorrect": 2,
        "bubble_correct": 3,
        "bubble_incorrect": 4,
    }
