import { useEffect, useState } from "react";
import { api, Round } from "../api/client";
import { ScorePanel } from "../components/ScorePanel";
import { SortBars } from "../components/SortBars";

type Props = { initialRound: Round; onExit: () => void };

export function GamePage({ initialRound, onExit }: Props) {
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
    if (result.next_round) setRound(result.next_round);
  }

  async function finish() {
    await api.finishGame(round.game_id);
    onExit();
  }

  return (
    <main className="page gameLayout">
      <section className="card gameCard">
        <div className="gameHeader">
          <div>
            <h2>{round.sorting_type.replaceAll("_", " ")}</h2>
            <p>{round.prompt}</p>
          </div>
          <strong className={seconds <= 5 ? "timer warning" : "timer"}>{seconds}s</strong>
        </div>

        {round.question_type === "TYPE_PASS_NUMBER" && round.target_array && (
          <>
            <h3>Original array</h3>
            <SortBars values={round.original_array} />
            <h3>Array shown</h3>
            <SortBars values={round.target_array} />
            <label className="passInput">Pass number
              <input type="number" min="1" value={answerPass} onChange={e => setAnswerPass(e.target.value)} />
            </label>
          </>
        )}

        {round.question_type === "ARRANGE_TO_PASS" && (
          <>
            <p className="hint">Use the arrow buttons to reorder the bars into the requested pass.</p>
            <SortBars values={answerArray} editable onChange={setAnswerArray} />
          </>
        )}

        {message && <div className={message.startsWith("Correct") ? "success" : "error"}>{message}</div>}
        <div className="actions">
          <button className="primary" onClick={submit}>Check answer</button>
          <button onClick={finish}>Finish game</button>
        </div>
      </section>
      <ScorePanel score={score} counters={counters} />
    </main>
  );
}
