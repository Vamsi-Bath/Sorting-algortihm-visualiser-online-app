import { useEffect, useState } from "react";
import { api, getToken, Round, User } from "./api/client";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { AuthPage } from "./pages/AuthPage";
import { DashboardPage } from "./pages/DashboardPage";
import { GamePage } from "./pages/GamePage";
import { LeaderboardPage } from "./pages/LeaderboardPage";
import { MenuPage } from "./pages/MenuPage";
import "./styles/app.css";

type View = "auth" | "dashboard" | "menu" | "game" | "leaderboard" | "analytics";

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [view, setView] = useState<View>(getToken() ? "dashboard" : "auth");
  const [round, setRound] = useState<Round | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (getToken()) api.me().then(setUser).catch(() => setView("auth"));
  }, []);

  async function start(mode: string) {
    try {
      setError("");
      const newRound = await api.startGame(mode);
      setRound(newRound);
      setView("game");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not start game");
    }
  }

  function logout() {
    setUser(null);
    setRound(null);
    setView("auth");
  }

  if (view === "auth" || !user) return <AuthPage onAuth={(u) => { setUser(u); setView("dashboard"); }} />;

  const nav = {
    user,
    onDashboard: () => setView("dashboard" as View),
    onPlay: () => setView("menu" as View),
    onLeaderboard: () => setView("leaderboard" as View),
    onAnalytics: () => setView("analytics" as View),
    onLogout: logout
  };

  if (view === "game" && round) return <GamePage initialRound={round} onExit={() => setView("menu")} nav={nav} />;
  if (view === "leaderboard") return <LeaderboardPage nav={nav} />;
  if (view === "analytics") return <AnalyticsPage nav={nav} />;
  if (view === "menu") return <><MenuPage user={user} onStart={start} nav={nav} />{error && <div className="floatingError">{error}</div>}</>;

  return <><DashboardPage user={user} onStart={start} nav={nav} />{error && <div className="floatingError">{error}</div>}</>;
}
