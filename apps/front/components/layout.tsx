import { useRouter } from "next/router";
import { ReactElement } from "react";
import styles from "../styles/components/DefaultLayout.module.css";
import { Link } from "./link";

type DefaultLayoutProps = {
  children: ReactElement;
};

export function DefaultLayout({ children }: DefaultLayoutProps): ReactElement {
  const route = useRouter();
  if (route == null || !route.isReady) return <></>;

  return (
    <div className={styles.main}>
      <div className={styles.header}>
        <Link
          className={route.pathname === "/" ? styles.active : undefined}
          href="/"
        >
          <div>Customer Loyalty</div>
        </Link>
        <Link
          className={route.pathname === "/order" ? styles.active : undefined}
          href="/order"
        >
          <div>Order History</div>
        </Link>
      </div>
      <div className={styles.content}>{children}</div>
    </div>
  );
}
