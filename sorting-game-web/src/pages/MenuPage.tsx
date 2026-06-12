import { User, clearToken } from "../api/client";

type Props = {
  user: User;
  onStart: (mode: string) => void;
  onShowLeaderboard: () => void;
  onShowAnalytics: () => void;
  onLogout: () => void;
};

export function MenuPage({ user, onStart, onShowLeaderboard, onShowAnalytics, onLogout }: Props) {
  function logout() {
    clearToken();
    onLogout();
  }
  return (
    <main className="page narrow">
      <section className="hero card">
        <h1>Welcome, {user.username}</h1>
        <p>Class {user.class_name}</p>
        <div className="buttonGrid">
          <button className="primary" onClick={() => onStart("Randomized_Competitive")}>Randomized Competitive</button>
          <button onClick={() => onStart("Practice_Bubble")}>Practice Bubble Sort</button>
          <button onClick={() => onStart("Practice_Insertion")}>Practice Insertion Sort</button>
          <button onClick={onShowLeaderboard}>Leaderboard</button>
          <button onClick={onShowAnalytics}>Analytics</button>
          <button className="danger" onClick={logout}>Logout</button>
        </div>
      </section>
    </main>
  );
}
