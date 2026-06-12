def calculate_score(insertion_correct: int, insertion_incorrect: int, bubble_correct: int, bubble_incorrect: int) -> int:
    correct = insertion_correct + bubble_correct
    incorrect = insertion_incorrect + bubble_incorrect
    total = correct + incorrect
    if total == 0:
        return 0
    accuracy_points = round((correct / total) * 100)
    volume_bonus = correct * 5
    return accuracy_points + volume_bonus

def counters_dict(game) -> dict:
    return {
        "insertion_correct": game.insertion_correct,
        "insertion_incorrect": game.insertion_incorrect,
        "bubble_correct": game.bubble_correct,
        "bubble_incorrect": game.bubble_incorrect,
    }
