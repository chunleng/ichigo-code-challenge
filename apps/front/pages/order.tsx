import { DefaultLayout } from "components/layout";
import type { NextPage } from "next";
import styles from "../styles/Home.module.css";

const Home: NextPage = () => {
  return (
    <DefaultLayout>
      <div className={styles.main}>TEST</div>
    </DefaultLayout>
  );
};

export default Home;
