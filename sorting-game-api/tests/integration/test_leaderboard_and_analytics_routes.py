
def test_leaderboard_and_analytics_endpoints(client, auth_headers):
    start = client.post(
        "/games/start",
        json={"mode": "Practice_Bubble"},
        headers=auth_headers,
    ).json()
    client.post(f"/games/{start['game_id']}/finish", headers=auth_headers)

    leaderboard = client.get("/scores/leaderboard")
    assert leaderboard.status_code == 200
    assert isinstance(leaderboard.json(), list)

    mine = client.get("/scores/mine", headers=auth_headers)
    assert mine.status_code == 200
    assert len(mine.json()) >= 1

    classes = client.get("/analytics/classes", headers=auth_headers)
    assert classes.status_code == 200
    assert isinstance(classes.json(), list)

    sorting_types = client.get("/analytics/sorting-types", headers=auth_headers)
    assert sorting_types.status_code == 200
    assert set(sorting_types.json()) == {
        "insertion_correct",
        "insertion_incorrect",
        "bubble_correct",
        "bubble_incorrect",
    }
