type Props = {
  score: number;
  counters: Record<string, number>;
};

export function ScorePanel({ score, counters }: Props) {
  return (
    <aside className="card scorePanel">
      <h3>Score: {score}</h3>
      <p>Insertion correct: {counters.insertion_correct ?? 0}</p>
      <p>Insertion incorrect: {counters.insertion_incorrect ?? 0}</p>
      <p>Bubble correct: {counters.bubble_correct ?? 0}</p>
      <p>Bubble incorrect: {counters.bubble_incorrect ?? 0}</p>
    </aside>
  );
}
