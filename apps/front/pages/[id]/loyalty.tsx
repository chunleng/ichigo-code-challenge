import { AxiosResponse } from "axios";
import {
  CustomerLoyaltyInformation,
  DefaultApi,
} from "components/generated/api";
import { DefaultLayout } from "components/layout";
import { ProgressBar } from "components/progressbar";
import { Config } from "config/openapi";
import type { NextPage } from "next";
import { useRouter } from "next/router";
import { ReactElement, useEffect, useState } from "react";
import styles from "../../styles/pages/[id]/Loyalty.module.css";

const Loyalty: NextPage = () => {
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

  return <LoyaltyPanel customerId={id} />;
}
function LoyaltyPanel({ customerId }: { customerId: string }): ReactElement {
  const [loyaltyInformation, setLoyaltyInformation] =
    useState<CustomerLoyaltyInformation | null>();

  useEffect(() => {
    void new DefaultApi(Config())
      .getLoyaltyInformationByCustomer(customerId)
      .then(
        (value) => {
          setLoyaltyInformation(value.data);
        },
        ({ response }: { response?: AxiosResponse<unknown> }) => {
          if (response?.status === 404) setLoyaltyInformation(null);
        }
      );
  }, [customerId]);

  if (loyaltyInformation === undefined) return <></>;
  if (loyaltyInformation === null)
    return <div>Customer &quot;{customerId}&quot; does not exist!</div>;

  return (
    <>
      <div className={styles.summary}>
        Customer &quot;{customerId}&quot; is currently at&nbsp;
        <span
          className={`${styles.tier} ${
            styles[loyaltyInformation.current_tier]
          }`}
        >
          {loyaltyInformation.current_tier}
        </span>
      </div>
      <ProgressBar
        progress={
          loyaltyInformation.purchase_amount_in_cents /
          (loyaltyInformation.purchase_amount_to_next_tier_in_cents +
            loyaltyInformation.purchase_amount_in_cents)
        }
      />
      {loyaltyInformation.current_tier == "gold" ? null : (
        <div className={styles.footer}>
          $
          {(
            loyaltyInformation.purchase_amount_to_next_tier_in_cents / 100
          ).toLocaleString()}{" "}
          more to promotion!
        </div>
      )}
    </>
  );
}

export default Loyalty;
