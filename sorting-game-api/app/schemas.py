from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    username: str = Field(min_length=4, max_length=40)
    email: EmailStr
    class_name: str = Field(min_length=2, max_length=10)
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    token: str
    user: dict

class StartGameRequest(BaseModel):
    mode: str = "Randomized_Competitive"

class RoundResponse(BaseModel):
    game_id: int
    round_id: int
    mode: str
    sorting_type: str
    question_type: str
    original_array: list[int]
    target_pass_number: int | None = None
    target_array: list[int] | None = None
    prompt: str
    time_limit_seconds: int

class SubmitAnswerRequest(BaseModel):
    round_id: int
    answer_array: list[int] | None = None
    answer_pass_number: int | None = None

class SubmitAnswerResponse(BaseModel):
    correct: bool
    expected_array: list[int]
    expected_pass_number: int
    score: int
    counters: dict
    next_round: RoundResponse | None

class FinishGameResponse(BaseModel):
    game_id: int
    final_score: int
    counters: dict

class LeaderboardEntry(BaseModel):
    username: str
    class_name: str
    score: int
    game_id: int
