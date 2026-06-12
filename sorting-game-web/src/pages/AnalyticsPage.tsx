import { useEffect, useState } from "react";
import { api, User } from "../api/client";
import { Sidebar } from "../components/Sidebar";

type ClassRow = { class_name: string; games_played: number; average_score: number };
type Nav = { user: User; onDashboard: () => void; onPlay: () => void; onLeaderboard: () => void; onAnalytics: () => void; onLogout: () => void };

export function AnalyticsPage({ nav }: { nav: Nav }) {
  const [classes, setClasses] = useState<ClassRow[]>([]);
  const [sorting, setSorting] = useState<Record<string, number>>({});
  useEffect(() => { api.classAnalytics().then(setClasses); api.sortingAnalytics().then(setSorting); }, []);
  const totalGames = classes.reduce((sum, row) => sum + row.games_played, 0);
  const avg = classes.length ? Math.round(classes.reduce((sum, row) => sum + row.average_score, 0) / classes.length) : 0;
  return (
    <main className="appShell">
      <Sidebar active="analytics" {...nav} />
      <section className="contentArea">
        <h1>Class Analytics</h1><p>Overall performance of your class</p>
        <div className="statsGrid">
          <article className="statCard"><span>Class Average Score</span><strong>{avg}</strong></article>
          <article className="statCard"><span>Total Classes</span><strong>{classes.length}</strong></article>
          <article className="statCard"><span>Total Games Played</span><strong>{totalGames}</strong></article>
          <article className="statCard"><span>Highest Score</span><strong className="green">{Math.max(0, ...classes.map(row => row.average_score))}</strong></article>
        </div>
        <div className="dashboardGrid">
          <article className="whiteCard"><h2>Average Score Over Time</h2><div className="chartPlaceholder"><svg viewBox="0 0 350 190"><polyline points="10,55 80,110 150,115 220,145 280,105 330,95" fill="none" stroke="#6d28d9" strokeWidth="5"/><line x1="0" y1="170" x2="350" y2="170" stroke="#e5e7eb"/><line x1="20" y1="20" x2="20" y2="175" stroke="#e5e7eb"/></svg></div></article>
          <article className="whiteCard"><h2>Class Performance</h2><table className="lightTable"><tbody>{classes.map(row => <tr key={row.class_name}><td>{row.class_name}</td><td>{row.games_played} games</td><td>{row.average_score}</td></tr>)}</tbody></table>{classes.length === 0 && <p>No analytics yet.</p>}</article>
        </div>
        <h1>Sorting Analytics</h1>
        <div className="analyticsCards">{Object.entries(sorting).map(([key, value]) => <article className="whiteCard donutCard" key={key}><h2>{key.replaceAll("_", " ")}</h2><p>Total: {value}</p><div className="donut" /></article>)}</div>
      </section>
    </main>
  );
}
