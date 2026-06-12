import { User } from "../api/client";
import { Sidebar } from "../components/Sidebar";

type Nav = {
  user: User;
  onDashboard: () => void;
  onPlay: () => void;
  onLeaderboard: () => void;
  onAnalytics: () => void;
  onLogout: () => void;
};

type Props = { user: User; onStart: (mode: string) => void; nav: Nav };

export function DashboardPage({ user, onStart, nav }: Props) {
  return (
    <main className="appShell">
      <Sidebar active="dashboard" {...nav} />
      <section className="contentArea">
        <div className="topBar"><div><h1>Dashboard</h1><p>Welcome back, {user.username}!</p></div><span className="classPill">Class: {user.class_name}</span></div>
        <div className="statsGrid">
          <article className="statCard"><span>Total Games</span><strong>0</strong></article>
          <article className="statCard"><span>High Score</span><strong className="orange">0</strong></article>
          <article className="statCard"><span>Average Score</span><strong className="green">0</strong></article>
          <article className="statCard"><span>Total Points</span><strong className="purple">0</strong></article>
        </div>
        <div className="dashboardGrid">
          <article className="whiteCard">
            <h2>Recent Games</h2>
            <table><thead><tr><th>Date</th><th>Mode</th><th>Score</th><th>Details</th></tr></thead><tbody><tr><td>Today</td><td>Randomized Competitive</td><td>Start playing</td><td><button className="textLink" onClick={() => onStart("Randomized_Competitive")}>Play</button></td></tr></tbody></table>
          </article>
          <article className="whiteCard">
            <h2>Performance Overview</h2>
            <div className="chartPlaceholder"><svg viewBox="0 0 350 190" role="img" aria-label="Performance line chart"><polyline points="10,160 80,110 150,130 220,80 330,35" fill="none" stroke="#6d28d9" strokeWidth="5"/><line x1="0" y1="170" x2="350" y2="170" stroke="#e5e7eb"/><line x1="20" y1="20" x2="20" y2="175" stroke="#e5e7eb"/></svg></div>
          </article>
        </div>
      </section>
    </main>
  );
}
