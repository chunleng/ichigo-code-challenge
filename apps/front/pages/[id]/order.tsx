import { DefaultApi, OrderResponse } from "components/generated/api";
import { DefaultLayout } from "components/layout";
import { Config } from "config/openapi";
import type { NextPage } from "next";
import { useRouter } from "next/router";
import { ReactElement, useEffect, useState } from "react";
import styles from "../../styles/pages/[id]/Order.module.css";

const Order: NextPage = () => {
  return (
    <DefaultLayout>
      <Content />
    </DefaultLayout>
  );
};

function Content(): ReactElement {
  const router = useRouter();

  if (router == null || !router.isReady) return <></>;

  const { id } = router.query;
  if (typeof id !== "string") return <>Please input a valid customer ID</>;

  return <OrderPanel customerId={id} />;
}

function OrderPanel({ customerId }: { customerId: string }): ReactElement {
  const [orders, setOrders] = useState<OrderResponse[]>();

  useEffect(() => {
    void new DefaultApi(Config())
      .listOrdersByCustomerId(customerId)
      .then((value) => {
        setOrders(value.data);
      });
  }, [customerId]);

  if (orders == null) return <></>;

  return (
    <>
      <div className={styles.summary}>
        Order history of customer &quot;{customerId}&quot;
      </div>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>#</th>
            <th>Total ($)</th>
            <th>Purchase Date</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((value) => (
            <tr key={value.id}>
              <td>{value.id}</td>
              <td>{(value.total_in_cents / 100).toLocaleString()}</td>
              <td>{value.purchase_on}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

export default Order;
