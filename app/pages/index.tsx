import Head from 'next/head';
import Image from 'next/image';
import Layout from "components/layout";
import * as React from 'react';

import Map from 'components/map';
export default function Home() {
  return <Layout main={
    <>
      <Map />
    </>
  }></Layout>
}
