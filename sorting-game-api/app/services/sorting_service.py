import random
from dataclasses import dataclass

SORTING_TYPES = ["BUBBLE_SORT", "INSERTION_SORT"]
QUESTION_TYPES = ["ARRANGE_TO_PASS", "TYPE_PASS_NUMBER"]

@dataclass
class GeneratedRound:
    sorting_type: str
    question_type: str
    original_array: list[int]
    target_pass_number: int
    target_array: list[int]


def bubble_sort_passes(values: list[int]) -> list[list[int]]:
    arr = values[:]
    passes: list[list[int]] = []
    n = len(arr)
    swapped = True
    while n > 0 and swapped:
        swapped = False
        n -= 1
        for index in range(n):
            if arr[index] > arr[index + 1]:
                arr[index], arr[index + 1] = arr[index + 1], arr[index]
                swapped = True
        if arr not in passes:
            passes.append(arr[:])
    return passes or [arr]


def insertion_sort_passes(values: list[int]) -> list[list[int]]:
    arr = values[:]
    passes: list[list[int]] = []
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and current < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
        passes.append(arr[:])
    unique: list[list[int]] = []
    for item in passes:
        if item not in unique:
            unique.append(item)
    return unique or [arr]


def generate_round(mode: str = "Randomized_Competitive") -> GeneratedRound:
    length = random.randint(5, 10)
    original = [random.randint(1, 30) for _ in range(length)]
    sorting_type = random.choice(SORTING_TYPES) if mode == "Randomized_Competitive" else (
        "BUBBLE_SORT" if mode == "Practice_Bubble" else "INSERTION_SORT"
    )
    passes = bubble_sort_passes(original) if sorting_type == "BUBBLE_SORT" else insertion_sort_passes(original)
    pass_index = random.randrange(len(passes))
    target_array = passes[pass_index]
    question_type = random.choice(QUESTION_TYPES)
    return GeneratedRound(
        sorting_type=sorting_type,
        question_type=question_type,
        original_array=original,
        target_pass_number=pass_index + 1,
        target_array=target_array,
    )
