import { useEffect, useState } from "react";
import { api, getToken, Round, User } from "./api/client";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { AuthPage } from "./pages/AuthPage";
import { GamePage } from "./pages/GamePage";
import { LeaderboardPage } from "./pages/LeaderboardPage";
import { MenuPage } from "./pages/MenuPage";
import "./styles/app.css";

type View = "auth" | "menu" | "game" | "leaderboard" | "analytics";

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [view, setView] = useState<View>(getToken() ? "menu" : "auth");
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

  if (view === "auth" || !user) return <AuthPage onAuth={(u) => { setUser(u); setView("menu"); }} />;
  if (view === "game" && round) return <GamePage initialRound={round} onExit={() => setView("menu")} />;
  if (view === "leaderboard") return <LeaderboardPage onBack={() => setView("menu")} />;
  if (view === "analytics") return <AnalyticsPage onBack={() => setView("menu")} />;

  return <><MenuPage user={user} onStart={start} onShowLeaderboard={() => setView("leaderboard")} onShowAnalytics={() => setView("analytics")} onLogout={() => { setUser(null); setView("auth"); }} />{error && <div className="floatingError">{error}</div>}</>;
}
