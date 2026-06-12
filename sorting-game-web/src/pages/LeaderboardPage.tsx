import { useEffect, useState } from "react";
import { api, User } from "../api/client";
import { Sidebar } from "../components/Sidebar";

type Entry = { username: string; class_name: string; score: number; game_id: number };
type Nav = { user: User; onDashboard: () => void; onPlay: () => void; onLeaderboard: () => void; onAnalytics: () => void; onLogout: () => void };

export function LeaderboardPage({ nav }: { nav: Nav }) {
  const [entries, setEntries] = useState<Entry[]>([]);
  useEffect(() => { api.leaderboard().then(setEntries); }, []);
  return (
    <main className="appShell">
      <Sidebar active="leaderboard" {...nav} />
      <section className="contentArea">
        <h1>Leaderboard</h1><p>Top 5 Players</p>
        <article className="whiteCard">
          <table className="lightTable"><thead><tr><th>Rank</th><th>Username</th><th>Class</th><th>High Score</th><th>Total Games</th></tr></thead><tbody>{entries.map((entry, index) => <tr key={entry.game_id}><td>{index < 3 ? ["🥇","🥈","🥉"][index] : index + 1}</td><td>{entry.username}</td><td>{entry.class_name}</td><td>{entry.score}</td><td>1</td></tr>)}</tbody></table>
          {entries.length === 0 && <p>No scores yet.</p>}
        </article>
      </section>
    </main>
  );
}
