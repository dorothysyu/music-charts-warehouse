import React, { useState, useEffect } from 'react'
import './index.css'
import Header from './components/Header'
import Table from './components/Table'
import data from './data'

function App() {
  // const data = [
  //   { "Chart Name": "Billboard", "Chart Week": 1631923200000, "Title": "Way 2 Sexy", "Artist": "Drake Featuring Future & Young Thug", "Song ID": 290, "Position": 1, "Streams": 0, "Weeks on Chart": 1, "Peak Position": 1, "Last Position": 0 },
  //   { "Chart Name": "Billboard", "Chart Week": 1631923200000, "Title": "Girls Want Girls", "Artist": "Drake Featuring Lil Baby", "Song ID": 291, "Position": 2, "Streams": 0, "Weeks on Chart": 1, "Peak Position": 2, "Last Position": 0 },
  //   { "Chart Name": "Billboard", "Chart Week": 1631923200000, "Title": "Fair Trade", "Artist": "Drake Featuring Travis Scott", "Song ID": 292, "Position": 3, "Streams": 0, "Weeks on Chart": 1, "Peak Position": 3, "Last Position": 0 }, { "Chart Name": "Billboard", "Chart Week": 1631923200000, "Title": "Champagne Poetry", "Artist": "Drake", "Song ID": 293, "Position": 4, "Streams": 0, "Weeks on Chart": 1, "Peak Position": 4, "Last Position": 0 },
  //   {
  //     "Chart Name": "Billboard", "Chart Week": 1631923200000, "Title": "Knife Talk", "Artist": "Drake Featuring 21 Savage & Project Pat", "Song ID": 294, "Position": 5, "Streams": 0, "Weeks on Chart": 1, "Peak Position": 5, "Last Position": 0
  //   }]

  /*'Chart Name', 'Chart Week', 'Title', 'Artist', 'Song ID', 'Position', 'Streams',
  'Weeks on Chart', 'Peak Position', 'Last Position'*/
  const columns = [
    {
      Header: 'hi',
      columns: [
        {
          Header: "Chart Name",
          accessor: "Chart Name"
        },
        {
          Header: "Chart Week",
          accessor: "Chart Week"
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
      ]
    }
  ];

  return (
    <div className="container">
      <Header title='Music Chart Warehouse' />
      <Table columns={columns} data={data} />
    </div>
  );
}

export default App
