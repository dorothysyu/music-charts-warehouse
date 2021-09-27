import React, { useState, useEffect } from 'react'
import './index.css'
import Header from './components/Header'
import Table from './components/Table'
import data from './data'

function App() {
  /* Ensures that data isn't recreated on every render. */
  const reusableData = React.useMemo(
    () => data, []
  )

  const columns = React.useMemo(
    () => [
      // {
      //   Header: "Chart Name",
      //   accessor: "Chart Name",
      //   sortType: 'basic'
      // },
      {
        Header: "Chart Week",
        accessor: "Chart Week"
      },
      {
        Header: "Position",
        accessor: "Position"
      },
      {
        Header: "Title",
        accessor: "Title",
        sortType: 'basic'
      },
      {
        Header: "Artist",
        accessor: "Artist",
        sortType: 'basic'
      },
      // {
      //   Header: "Song ID",
      //   accessor: "Song ID"
      // },
      {
        Header: "Streams",
        accessor: "Streams",
        sortType: 'basic'
      },
      {
        Header: "Weeks on Chart",
        accessor: "Weeks on Chart",
        sortType: 'basic'
      },
      {
        Header: "Peak Position",
        accessor: "Peak Position",
        sortType: 'basic'
      },
      {
        Header: "Last Position",
        accessor: "Last Position",
        sortType: 'basic'
      },
    ],
    []
  )

  return (
    <div className="container">
      <Header title='Music Chart Warehouse' />
      <Table columns={columns} data={reusableData} />
    </div>
  );
}

export default App
