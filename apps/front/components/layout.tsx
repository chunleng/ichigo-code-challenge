import { useRouter } from "next/router";
import { ReactElement } from "react";
import styles from "../styles/components/DefaultLayout.module.css";
import { Link } from "./link";

type DefaultLayoutProps = {
  children: ReactElement;
};

export function DefaultLayout({ children }: DefaultLayoutProps): ReactElement {
  const router = useRouter();
  if (router == null || !router.isReady) return <></>;

  let { id } = router.query;
  if (typeof id !== "string") id = "";

  return (
    <div className={styles.main}>
      <div className={styles.header}>
        <Link
          className={
            router.pathname.endsWith("/loyalty") ? styles.active : undefined
          }
          href={`/${id}/loyalty`}
        >
          <div>Customer Loyalty</div>
        </Link>
        <Link
          className={
            router.pathname.endsWith("/order") ? styles.active : undefined
          }
          href={`/${id}/order`}
        >
          <div>Order History</div>
        </Link>
      </div>
      <div className={styles.content}>
        <div className={styles.mainPanel}>{children}</div>
      </div>
    </div>
  );
}
