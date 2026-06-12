type Props = { score: number; counters: Record<string, number> };

export function ScorePanel({ score, counters }: Props) {
  const insertionCorrect = counters.insertion_correct ?? 0;
  const insertionIncorrect = counters.insertion_incorrect ?? 0;
  const bubbleCorrect = counters.bubble_correct ?? 0;
  const bubbleIncorrect = counters.bubble_incorrect ?? 0;
  const total = insertionCorrect + insertionIncorrect + bubbleCorrect + bubbleIncorrect;
  const correct = insertionCorrect + bubbleCorrect;
  const accuracy = total === 0 ? 0 : Math.round((correct / total) * 100);

  return (
    <aside className="scorePanel card smallCard">
      <h2>Score: {score}</h2>
      <div className="scoreGrid">
        <span>Insertion correct: {insertionCorrect}</span>
        <span>Insertion incorrect: {insertionIncorrect}</span>
        <span>Bubble correct: {bubbleCorrect}</span>
        <span>Bubble incorrect: {bubbleIncorrect}</span>
      </div>
      <div className="accuracyBox">
        <strong>{accuracy}%</strong>
        <span>Accuracy</span>
      </div>
    </aside>
  );
}
