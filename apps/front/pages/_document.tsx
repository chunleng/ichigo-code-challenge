import { Head, Html, Main, NextScript } from "next/document";
import { ReactElement } from "react";

export default function Document(): ReactElement {
  return (
    <Html>
      <Head>
        <title>Ichigo Inc.</title>
        <meta name="description" content="Ichigo Loyalty Program" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
