/*Thank u to https://blog.logrocket.com/building-styling-tables-react-table-v7/ */
import { useTable, useSortBy, useFilters } from "react-table";

const Table = ({ columns, data }) => {
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow
    } = useTable({
        columns,
        data
    },
        useFilters,
        useSortBy);

    return (
        <table {...getTableProps()}>
            <thead>
                {headerGroups.map(headerGroup => (
                    <tr
                        className='table-header'
                        {...headerGroup.getHeaderGroupProps()}>
                        {headerGroup.headers.map(column => (
                            <th
                                className='columnTitleCell'
                                {...column.getHeaderProps(column.getSortByToggleProps())}>
                                {column.render("Header")}
                                {/* Add sorting indicator. */}
                                <span>
                                    {column.isSorted
                                        ? column.isSortedDesc ? '▼' : '▲'
                                        : ''}
                                </span>
                            </th>
                        ))}
                    </tr>
                ))}
            </thead>
            <tbody className='tableBody'
                {...getTableBodyProps()}>
                {rows.map((row, i) => {
                    prepareRow(row);
                    return (
                        <tr
                            className='track-row'
                            {...row.getRowProps()}>
                            {row.cells.map(cell => {
                                return <td
                                    className='track-cell'
                                    {...cell.getCellProps()}>{cell.render("Cell")}</td>;
                            })}
                        </tr>
                    );
                })}
            </tbody>
        </table>
    );
};

export default Table
