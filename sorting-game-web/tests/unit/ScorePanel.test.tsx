import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { ScorePanel } from '../../src/components/ScorePanel';

describe('ScorePanel', () => {
  it('renders score and counters', () => {
    render(
      <ScorePanel
        score={120}
        counters={{
          insertion_correct: 1,
          insertion_incorrect: 2,
          bubble_correct: 3,
          bubble_incorrect: 4,
        }}
      />,
    );

    expect(screen.getByText('Score: 120')).toBeInTheDocument();
    expect(screen.getByText('Insertion correct: 1')).toBeInTheDocument();
    expect(screen.getByText('Bubble incorrect: 4')).toBeInTheDocument();
  });

  it('defaults missing counters to zero', () => {
    render(<ScorePanel score={0} counters={{}} />);
    expect(screen.getByText('Insertion correct: 0')).toBeInTheDocument();
    expect(screen.getByText('Bubble incorrect: 0')).toBeInTheDocument();
  });
});
