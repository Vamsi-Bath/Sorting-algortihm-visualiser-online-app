const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export type User = { id: number; username: string; email: string; class_name: string };
export type Round = {
  game_id: number;
  round_id: number;
  mode: string;
  sorting_type: string;
  question_type: "ARRANGE_TO_PASS" | "TYPE_PASS_NUMBER";
  original_array: number[];
  target_pass_number: number | null;
  target_array: number[] | null;
  prompt: string;
  time_limit_seconds: number;
};

export type SubmitResult = {
  correct: boolean;
  expected_array: number[];
  expected_pass_number: number;
  score: number;
  counters: Record<string, number>;
  next_round: Round | null;
};

export function getToken() {
  return localStorage.getItem("token");
}

export function setToken(token: string) {
  localStorage.setItem("token", token);
}

export function clearToken() {
  localStorage.removeItem("token");
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers ?? {})
    }
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || "Something went wrong");
  }
  return response.json();
}

export const api = {
  register: (payload: { username: string; email: string; class_name: string; password: string }) =>
    request<{ token: string; user: User }>("/auth/register", { method: "POST", body: JSON.stringify(payload) }),
  login: (payload: { username: string; password: string }) =>
    request<{ token: string; user: User }>("/auth/login", { method: "POST", body: JSON.stringify(payload) }),
  me: () => request<User>("/auth/me"),
  startGame: (mode: string) => request<Round>("/games/start", { method: "POST", body: JSON.stringify({ mode }) }),
  submitAnswer: (gameId: number, payload: { round_id: number; answer_array?: number[]; answer_pass_number?: number }) =>
    request<SubmitResult>(`/games/${gameId}/submit-answer`, { method: "POST", body: JSON.stringify(payload) }),
  finishGame: (gameId: number) => request<{ game_id: number; final_score: number; counters: Record<string, number> }>(`/games/${gameId}/finish`, { method: "POST" }),
  leaderboard: () => request<Array<{ username: string; class_name: string; score: number; game_id: number }>>("/scores/leaderboard"),
  classAnalytics: () => request<Array<{ class_name: string; games_played: number; average_score: number }>>("/analytics/classes"),
  sortingAnalytics: () => request<Record<string, number>>("/analytics/sorting-types")
};
