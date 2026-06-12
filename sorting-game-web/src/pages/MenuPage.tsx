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

export function MenuPage({ onStart, nav }: Props) {
  return (
    <main className="appShell">
      <Sidebar active="play" {...nav} />
      <section className="contentArea">
        <h1>Play Game</h1>
        <p>Choose your game mode.</p>
        <div className="modeGrid">
          <article className="modeCard"><div className="modeIcon purpleIcon">♟</div><h2>Randomized Competitive</h2><p>Play timed rounds of Bubble Sort and Insertion Sort. Earn points and compete!</p><button className="primary wide" onClick={() => onStart("Randomized_Competitive")}>Start Game</button></article>
          <article className="modeCard"><div className="modeIcon greenIcon">☰</div><h2>Practice Bubble Sort</h2><p>Focus on Bubble Sort passes without competitive pressure.</p><button className="greenButton wide" onClick={() => onStart("Practice_Bubble")}>Start Game</button></article>
          <article className="modeCard"><div className="modeIcon blueIcon">☷</div><h2>Practice Insertion Sort</h2><p>Focus on Insertion Sort pass recognition and reordering.</p><button className="blueButton wide" onClick={() => onStart("Practice_Insertion")}>Start Game</button></article>
        </div>
        <article className="helpCard">
          <h3>How to Play</h3>
          <p>You will be given an array and a sorting algorithm. Either recreate the array after the given pass by dragging bars, or identify which pass number produced the target array.</p>
          <p>Earn points for correct answers and climb the leaderboard.</p>
        </article>
      </section>
    </main>
  );
}
