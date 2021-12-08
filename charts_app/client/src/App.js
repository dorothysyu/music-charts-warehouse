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
        () => [{
            Header: "Chart Name",
            accessor: "Chart Name",
            show: false
        },
        {
            Header: "Chart Week",
            accessor: "Chart Week",
            show: false,
            Cell: ({ value }) => { return format(new Date(value), 'MMM d, Y') }
        },
        {
            Header: "",
            accessor: "Position",
            className: "number"
        },
        {
            Header: "",
            accessor: "Title",
            className: "title"
        },
        {
            Header: "",
            accessor: "Artist",
            className: "artist"
        },
        {
            Header: "Song ID",
            accessor: "Song ID",
            show: false
        },
        {
            Header: "Spotify Streams",
            accessor: "Streams",
            className: "track-cell number",
            Cell: ({ value }) => {
                const disp = value > 0 ? value.toLocaleString() : '-'
                return disp
            }
        },
        {
            Header: "Billboard Weeks on Chart",
            accessor: "Weeks on Chart",
            className: "number",
            Cell: ({ value }) => {
                const disp = value > 0 ? value : '-'
                return disp
            }
        },
        {
            Header: "Billboard Peak Position",
            accessor: "Peak Position",
            className: "number",
            Cell: ({ value }) => {
                const disp = value > 0 ? value : '-'
                return disp
            }
        },
        {
            Header: "Billboard Last Position",
            accessor: "Last Position",
            className: "number",
            Cell: ({ value }) => {
                const disp = value > 0 ? value : '-'
                return disp
            }
        },
        ], []
    )

    return (
        <div className="container">
            <Header title='Music Chart Warehouse' />
            <Table columns={columns} data={reusableData} />
        </div>
    );
}

export default App