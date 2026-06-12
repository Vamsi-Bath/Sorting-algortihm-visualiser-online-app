import { clearToken, User } from "../api/client";

type Props = {
  user?: User | null;
  active: "dashboard" | "play" | "leaderboard" | "analytics";
  onDashboard: () => void;
  onPlay: () => void;
  onLeaderboard: () => void;
  onAnalytics: () => void;
  onLogout: () => void;
};

export function Sidebar({ active, user, onDashboard, onPlay, onLeaderboard, onAnalytics, onLogout }: Props) {
  function logout() {
    clearToken();
    onLogout();
  }

  return (
    <aside className="sidebar">
      <div className="brandRow">
        <div className="brandIcon">&lt;/&gt;</div>
        <div>
          <strong>Sorting Game</strong>
          <span>Master Algorithms</span>
        </div>
      </div>
      <nav className="sideNav" aria-label="Main navigation">
        <button className={active === "dashboard" ? "active" : ""} onClick={onDashboard}>▦ Dashboard</button>
        <button className={active === "play" ? "active" : ""} onClick={onPlay}>◎ Play Game</button>
        <button className={active === "leaderboard" ? "active" : ""} onClick={onLeaderboard}>♕ Leaderboard</button>
        <button className={active === "analytics" ? "active" : ""} onClick={onAnalytics}>▧ Analytics</button>
      </nav>
      {user && <div className="sidebarUser">Class: {user.class_name}</div>}
      <button className="logoutButton" onClick={logout}>↳ Logout</button>
    </aside>
  );
}
