import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { SortBars } from '../../src/components/SortBars';

describe('SortBars drag and drop interaction', () => {
  it('reorders bars when editable bars are dragged and dropped', () => {
    const onChange = vi.fn();
    render(<SortBars values={[3, 1, 2]} editable onChange={onChange} />);

    const bars = screen.getAllByTitle('Drag this bar to reorder it');
    const dataTransfer = {
      data: {} as Record<string, string>,
      setData(type: string, value: string) { this.data[type] = value; },
      getData(type: string) { return this.data[type]; },
      effectAllowed: 'move',
    };

    fireEvent.dragStart(bars[0], { dataTransfer });
    fireEvent.dragOver(bars[1], { dataTransfer });
    fireEvent.drop(bars[1], { dataTransfer });

    expect(onChange).toHaveBeenCalledWith([1, 3, 2]);
  });

  it('does not make bars draggable when read only', () => {
    render(<SortBars values={[3, 1, 2]} />);
    expect(screen.queryByTitle('Drag this bar to reorder it')).not.toBeInTheDocument();
  });
});
