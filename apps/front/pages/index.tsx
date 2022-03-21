import type { NextPage } from 'next'
import Head from 'next/head'
import styles from '../styles/Home.module.css'

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>Ichigo Inc.</title>
        <meta name="description" content="Ichigo Loyalty Program" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className={styles.main}>
        TEST
      </div>
    </>
  )
}

export default Home
