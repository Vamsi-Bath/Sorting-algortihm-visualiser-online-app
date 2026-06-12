type Props = {
  values: number[];
  editable?: boolean;
  onChange?: (values: number[]) => void;
};

export function SortBars({ values, editable = false, onChange }: Props) {
  const max = Math.max(...values, 1);

  function move(index: number, direction: -1 | 1) {
    if (!editable) return;
    const next = [...values];
    const target = index + direction;
    if (target < 0 || target >= next.length) return;
    [next[index], next[target]] = [next[target], next[index]];
    onChange?.(next);
  }

  return (
    <div className="bars" aria-label="sorting bars">
      {values.map((value, index) => (
        <div className="barBox" key={`${value}-${index}`}>
          <div className="bar" style={{ height: `${Math.max(16, (value / max) * 220)}px` }}>
            <span>{value}</span>
          </div>
          {editable && (
            <div className="barControls">
              <button onClick={() => move(index, -1)} disabled={index === 0}>←</button>
              <button onClick={() => move(index, 1)} disabled={index === values.length - 1}>→</button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
