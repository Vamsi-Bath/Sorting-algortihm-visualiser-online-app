import { useEffect, useState } from "react";
import { api } from "../api/client";

type ClassRow = { class_name: string; games_played: number; average_score: number };

export function AnalyticsPage({ onBack }: { onBack: () => void }) {
  const [classes, setClasses] = useState<ClassRow[]>([]);
  const [sorting, setSorting] = useState<Record<string, number>>({});
  useEffect(() => {
    api.classAnalytics().then(setClasses);
    api.sortingAnalytics().then(setSorting);
  }, []);
  return (
    <main className="page">
      <section className="card">
        <h1>Analytics</h1>
        <h2>Class performance</h2>
        <table>
          <thead><tr><th>Class</th><th>Games played</th><th>Average score</th></tr></thead>
          <tbody>{classes.map(row => <tr key={row.class_name}><td>{row.class_name}</td><td>{row.games_played}</td><td>{row.average_score}</td></tr>)}</tbody>
        </table>
        <h2>Sorting answers</h2>
        <div className="analyticsGrid">
          {Object.entries(sorting).map(([key, value]) => <div className="metric" key={key}><span>{key.replaceAll("_", " ")}</span><strong>{value}</strong></div>)}
        </div>
        <button onClick={onBack}>Back</button>
      </section>
    </main>
  );
}
