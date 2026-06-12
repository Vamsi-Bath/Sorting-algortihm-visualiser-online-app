import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { SortBars } from '../../src/components/SortBars';

describe('SortBars interaction', () => {
  it('moves bars when editable', () => {
    const onChange = vi.fn();
    render(<SortBars values={[3, 1, 2]} editable onChange={onChange} />);

    const rightButtons = screen.getAllByText('→');
    fireEvent.click(rightButtons[0]);

    expect(onChange).toHaveBeenCalledWith([1, 3, 2]);
  });

  it('does not show move controls when read only', () => {
    render(<SortBars values={[3, 1, 2]} />);
    expect(screen.queryByText('→')).not.toBeInTheDocument();
  });
});
