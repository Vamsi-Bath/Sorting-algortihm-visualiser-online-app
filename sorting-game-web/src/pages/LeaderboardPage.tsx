import { useEffect, useState } from "react";
import { api } from "../api/client";

type Entry = { username: string; class_name: string; score: number; game_id: number };

export function LeaderboardPage({ onBack }: { onBack: () => void }) {
  const [entries, setEntries] = useState<Entry[]>([]);
  useEffect(() => { api.leaderboard().then(setEntries); }, []);
  return (
    <main className="page narrow">
      <section className="card">
        <h1>Top 5 Leaderboard</h1>
        <table>
          <thead><tr><th>#</th><th>User</th><th>Class</th><th>Score</th></tr></thead>
          <tbody>{entries.map((entry, index) => <tr key={entry.game_id}><td>{index + 1}</td><td>{entry.username}</td><td>{entry.class_name}</td><td>{entry.score}</td></tr>)}</tbody>
        </table>
        {entries.length === 0 && <p>No scores yet.</p>}
        <button onClick={onBack}>Back</button>
      </section>
    </main>
  );
}
