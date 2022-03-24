import {
  CustomerLoyaltyInformation,
  DefaultApi,
} from "components/generated/api";
import { DefaultLayout } from "components/layout";
import { ProgressBar } from "components/progressbar";
import { Config } from "config/openapi";
import type { NextPage } from "next";
import { ReactElement, useEffect, useState } from "react";
import styles from "../styles/Home.module.css";

const Home: NextPage = () => {
  return (
    <DefaultLayout>
      <LoyaltyPanel customerId="3" />
    </DefaultLayout>
  );
};

function LoyaltyPanel({ customerId }: { customerId: string }): ReactElement {
  const [loyaltyInformation, setLoyaltyInformation] =
    useState<CustomerLoyaltyInformation>();

  useEffect(() => {
    void new DefaultApi(Config())
      .getLoyaltyInformationByCustomer(customerId)
      .then((value) => {
        setLoyaltyInformation(value.data);
      });
  }, [customerId]);

  if (loyaltyInformation == null) return <></>;

  return (
    <div className={styles.mainPanel}>
      <div className={styles.summary}>
        Customer #{customerId} is currently at&nbsp;
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
      <div className={styles.footer}>
        $
        {(
          loyaltyInformation.purchase_amount_to_next_tier_in_cents / 100
        ).toLocaleString()}{" "}
        more to promotion!
      </div>
    </div>
  );
}

export default Home;
