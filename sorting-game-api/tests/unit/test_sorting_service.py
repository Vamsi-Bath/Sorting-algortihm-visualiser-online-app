from app.services.sorting_service import (
    bubble_sort_passes,
    generate_round,
    insertion_sort_passes,
)


def test_bubble_sort_passes_end_sorted():
    passes = bubble_sort_passes([5, 2, 4])
    assert passes[-1] == [2, 4, 5]


def test_bubble_sort_passes_already_sorted_branch():
    passes = bubble_sort_passes([1, 2, 3])
    assert passes == [[1, 2, 3]]


def test_insertion_sort_passes_end_sorted():
    passes = insertion_sort_passes([5, 2, 4])
    assert passes[-1] == [2, 4, 5]


def test_insertion_sort_passes_already_sorted_branch():
    passes = insertion_sort_passes([1, 2, 3])
    assert passes == [[1, 2, 3]]


def test_generate_practice_bubble_round_uses_bubble_sort():
    round_ = generate_round("Practice_Bubble")
    assert round_.sorting_type == "BUBBLE_SORT"
    assert round_.target_pass_number >= 1
    assert len(round_.original_array) >= 5


def test_generate_practice_insertion_round_uses_insertion_sort():
    round_ = generate_round("Practice_Insertion")
    assert round_.sorting_type == "INSERTION_SORT"
    assert round_.question_type in {"ARRANGE_TO_PASS", "TYPE_PASS_NUMBER"}
