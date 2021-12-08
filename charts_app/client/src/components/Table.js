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
        data,
        initialState: {
            hiddenColumns: columns.map(column => {
                if (column.show == false) return column.accessor || column.id;
            }),
        }
    },
        useFilters,
        useSortBy);

    return (<table {...getTableProps()} >
        <thead > {
            headerGroups.map(headerGroup => (<tr {...headerGroup.getHeaderGroupProps()} > {
                headerGroup.headers.map(column => (< th {...column.getHeaderProps(column.getSortByToggleProps())} > {column.render("Header")} { /* Add sorting indicator. */} <
                    span > {
                        column.isSorted ?
                            column.isSortedDesc ? '▼' : '▲' : ''
                    } </span> </th >
                ))
            } </tr>
            ))
        } </thead>
        <tbody className='chart-table' {...getTableBodyProps()} > {
            rows.map((row, i) => {
                prepareRow(row);
                return (<tr {...row.getRowProps()} > {
                    row.cells.map(cell => {
                        return <td {...cell.getCellProps([{
                            className: cell.column.className
                        }])
                        } > {cell.render("Cell")} </td>;
                    })
                } </tr>
                );
            })
        } </tbody> </table >
    );
};

export default Table