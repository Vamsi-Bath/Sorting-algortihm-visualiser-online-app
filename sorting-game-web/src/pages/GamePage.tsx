import { useEffect, useState } from "react";
import { api, Round, User } from "../api/client";
import { ScorePanel } from "../components/ScorePanel";
import { Sidebar } from "../components/Sidebar";
import { SortBars } from "../components/SortBars";

type Nav = {
  user: User;
  onDashboard: () => void;
  onPlay: () => void;
  onLeaderboard: () => void;
  onAnalytics: () => void;
  onLogout: () => void;
};

type Props = { initialRound: Round; onExit: () => void; nav: Nav };

export function GamePage({ initialRound, onExit, nav }: Props) {
  const [round, setRound] = useState(initialRound);
  const [answerArray, setAnswerArray] = useState(initialRound.original_array);
  const [answerPass, setAnswerPass] = useState("");
  const [score, setScore] = useState(0);
  const [counters, setCounters] = useState<Record<string, number>>({});
  const [message, setMessage] = useState("");
  const [seconds, setSeconds] = useState(initialRound.time_limit_seconds);

  useEffect(() => {
    setAnswerArray(round.original_array);
    setAnswerPass("");
    setSeconds(round.time_limit_seconds);
    setMessage("");
  }, [round]);

  useEffect(() => {
    const id = window.setInterval(() => setSeconds(s => Math.max(0, s - 1)), 1000);
    return () => window.clearInterval(id);
  }, []);

  async function submit() {
    const payload = round.question_type === "ARRANGE_TO_PASS"
      ? { round_id: round.round_id, answer_array: answerArray }
      : { round_id: round.round_id, answer_pass_number: Number(answerPass) };
    const result = await api.submitAnswer(round.game_id, payload);
    setScore(result.score);
    setCounters(result.counters);
    setMessage(result.correct ? "Correct!" : `Incorrect. Expected pass ${result.expected_pass_number}: [${result.expected_array.join(", ")}]`);
    if (result.next_round) window.setTimeout(() => setRound(result.next_round!), 550);
  }

  async function finish() {
    await api.finishGame(round.game_id);
    onExit();
  }

  const algorithm = round.sorting_type.replaceAll("_", " ");
  const isGuess = round.question_type === "TYPE_PASS_NUMBER";

  return (
    <main className="appShell">
      <Sidebar active="play" {...nav} />
      <section className="contentArea gameContent">
        <div className="gameTopLine"><button className="exitSmall" onClick={finish}>× Exit Game</button><span>Game in Progress</span></div>
        <div className="roundStats">
          <article><span>Round</span><strong>{round.round_id}</strong></article>
          <article><span>Algorithm</span><strong>{algorithm}</strong></article>
          <article><span>Task</span><strong>{isGuess ? "Guess Pass" : "Recreate Pass"}</strong></article>
          <article><span>Score</span><strong className="greenText">{score}</strong></article>
          <article><span>Time Left</span><strong className={seconds <= 5 ? "redText" : ""}>{seconds}s</strong></article>
        </div>

        <div className="gameWorkspace">
          <section className="whiteCard playArea">
            {!isGuess && (
              <>
                <SortBars values={round.original_array} label="Original Array" />
                <h3 className="taskHeading">Recreate the array after pass {round.target_pass_number}</h3>
                <SortBars values={answerArray} editable onChange={setAnswerArray} label="Drag the rectangular bars into the correct order" />
              </>
            )}
            {isGuess && round.target_array && (
              <>
                <div className="twoColumnBars">
                  <SortBars values={round.original_array} label="Original Array (Pass 0)" />
                  <div className="arrowBetween">→</div>
                  <SortBars values={round.target_array} label="Array After Some Pass" />
                </div>
                <article className="answerCard">
                  <h3>Type what pass this is: {algorithm}</h3>
                  <p>Which pass number results in the array shown on the right?</p>
                  <label>Your Answer<input type="number" min="1" value={answerPass} onChange={e => setAnswerPass(e.target.value)} placeholder="Enter pass number" /></label>
                </article>
              </>
            )}
            {message && <div className={message.startsWith("Correct") ? "success" : "error"}>{message}</div>}
            <div className="actions"><button className="primary" onClick={submit}>✓ Submit Answer</button><button onClick={finish}>Finish Game</button></div>
          </section>
          <ScorePanel score={score} counters={counters} />
        </div>
        <div className="tipStrip">ⓘ Tip: In Bubble Sort, the largest unsorted element bubbles to its correct position at the end of each pass.</div>
      </section>
    </main>
  );
}
