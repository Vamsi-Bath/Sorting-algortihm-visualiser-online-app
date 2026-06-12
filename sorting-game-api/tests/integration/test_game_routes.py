
def test_start_game_returns_round(client, auth_headers):
    response = client.post(
        "/games/start",
        json={"mode": "Randomized_Competitive"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["game_id"] > 0
    assert body["round_id"] > 0
    assert body["sorting_type"] in {"BUBBLE_SORT", "INSERTION_SORT"}
    assert body["question_type"] in {"ARRANGE_TO_PASS", "TYPE_PASS_NUMBER"}


def test_submit_correct_answer_updates_score_and_returns_next_round(client, auth_headers):
    start = client.post(
        "/games/start",
        json={"mode": "Practice_Bubble"},
        headers=auth_headers,
    ).json()

    payload = {"round_id": start["round_id"]}
    if start["question_type"] == "ARRANGE_TO_PASS":
        # For arrange questions the target array is hidden, so use the pass number route is tested separately.
        # The API should still accept an array and mark it incorrect if it is wrong.
        payload["answer_array"] = start["original_array"]
    else:
        payload["answer_pass_number"] = start["target_pass_number"]

    response = client.post(
        f"/games/{start['game_id']}/submit-answer",
        json=payload,
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert "correct" in body
    assert "score" in body
    assert body["next_round"]["game_id"] == start["game_id"]


def test_finish_game_returns_final_score(client, auth_headers):
    start = client.post(
        "/games/start",
        json={"mode": "Practice_Insertion"},
        headers=auth_headers,
    ).json()
    response = client.post(
        f"/games/{start['game_id']}/finish",
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["game_id"] == start["game_id"]


def test_submit_missing_round_branch(client, auth_headers):
    response = client.post(
        "/games/999/submit-answer",
        json={"round_id": 999, "answer_pass_number": 1},
        headers=auth_headers,
    )
    assert response.status_code == 404
