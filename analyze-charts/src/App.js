import React, { useState, useEffect } from 'react'
import './index.css'
import Header from './components/Header'
import Table from './components/Table'
import data from './data'
import { format } from 'date-fns'

function App() {
  /* Ensures that data isn't recreated on every render. */
  const reusableData = React.useMemo(
    () => data, []
  )

  const columns = React.useMemo(
    () => [
      {
        Header: "Chart Name",
        accessor: "Chart Name",
        isVisible: false
      },
      {
        Header: "Chart Week",
        accessor: "Chart Week",
        Cell: ({ value }) => { return format(new Date(value), 'MMM d, Y') }
      },
      {
        Header: "Position",
        accessor: "Position"
      },
      {
        Header: "Title",
        accessor: "Title"
      },
      {
        Header: "Artist",
        accessor: "Artist"
      },
      {
        Header: "Song ID",
        accessor: "Song ID"
      },
      {
        Header: "Streams",
        accessor: "Streams"
      },
      {
        Header: "Weeks on Chart",
        accessor: "Weeks on Chart"
      },
      {
        Header: "Peak Position",
        accessor: "Peak Position"
      },
      {
        Header: "Last Position",
        accessor: "Last Position"
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
