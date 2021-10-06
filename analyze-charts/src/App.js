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
        accessor: "Position",
        className: "number"
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
        accessor: "Streams",
        className: "track-cell number",
        Cell: ({ value }) => {
          const disp = value > 0 ? value.toLocaleString() : '-'
          return disp
        }
      },
      {
        Header: "Weeks on Chart",
        accessor: "Weeks on Chart",
        className: "number",
        Cell: ({ value }) => {
          const disp = value > 0 ? value : '-'
          return disp
        }
      },
      {
        Header: "Peak Position",
        accessor: "Peak Position",
        className: "number",
        Cell: ({ value }) => {
          const disp = value > 0 ? value : '-'
          return disp
        }
      },
      {
        Header: "Last Position",
        accessor: "Last Position",
        className: "number",
        Cell: ({ value }) => {
          const disp = value > 0 ? value : '-'
          return disp
        }
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
