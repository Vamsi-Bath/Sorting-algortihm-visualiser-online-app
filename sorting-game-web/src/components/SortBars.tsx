type Props = {
  values: number[];
  editable?: boolean;
  onChange?: (values: number[]) => void;
  label?: string;
};

const palette = ["#ef4444", "#f59e0b", "#22c55e", "#3b82f6", "#7c3aed", "#14b8a6", "#ec4899", "#64748b"];

export function SortBars({ values, editable = false, onChange, label }: Props) {
  const max = Math.max(...values, 1);

  function reorder(fromIndex: number, toIndex: number) {
    if (!editable || fromIndex === toIndex || toIndex < 0 || toIndex >= values.length) return;
    const next = [...values];
    const [removed] = next.splice(fromIndex, 1);
    next.splice(toIndex, 0, removed);
    onChange?.(next);
  }

  return (
    <div className="barsPanel">
      {label && <h3>{label}</h3>}
      <div className={editable ? "bars draggableBars" : "bars"} aria-label={editable ? "draggable sorting bars" : "sorting bars"}>
        {values.map((value, index) => (
          <div
            className={editable ? "barBox draggable" : "barBox"}
            key={`${value}-${index}`}
            draggable={editable}
            onDragStart={(event) => {
              event.dataTransfer.setData("text/plain", String(index));
              event.dataTransfer.effectAllowed = "move";
            }}
            onDragOver={(event) => {
              if (editable) event.preventDefault();
            }}
            onDrop={(event) => {
              event.preventDefault();
              const fromIndex = Number(event.dataTransfer.getData("text/plain"));
              reorder(fromIndex, index);
            }}
            title={editable ? "Drag this bar to reorder it" : undefined}
          >
            <strong className="barValue">{value}</strong>
            <div
              className="bar"
              style={{
                height: `${Math.max(28, (value / max) * 230)}px`,
                background: palette[index % palette.length]
              }}
            />
            <span className="barIndex">{index}</span>
          </div>
        ))}
      </div>
      {editable && <p className="dragHint">Drag and drop the rectangular bars to change the order.</p>}
    </div>
  );
}
