import { ReactElement } from "react";
import style from "../styles/components/ProgressBar.module.css";

export function ProgressBar({ progress }: { progress: number }): ReactElement {
  const percentage = (Math.round(progress * 1000) / 10).toString() + "%";
  return (
    <div className={style.bar}>
      <div className={style.progress} style={{ width: percentage }}>
        <span>{percentage}</span>
      </div>
    </div>
  );
}
