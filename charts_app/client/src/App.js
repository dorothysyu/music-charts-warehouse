import React, { useState, useEffect } from 'react'
import './index.css'
import Header from './components/Header'
import { COLUMNS } from './components/Columns'
import Table from './components/Table'
import data from './data'

function App() {
    const columns = React.useMemo(() => COLUMNS, [])

    /* Ensures that data isn't recreated on every render. */
    const reusableData = React.useMemo(() => data, [])


    return (
        <div className="container">
            <Header title='Music Chart Warehouse' />
            <Table columns={columns} data={reusableData} />
        </div>
    );
}

export default App