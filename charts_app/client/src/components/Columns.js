import ColumnFilter from "./ColumnFilter"
import { format } from 'date-fns'

export const COLUMNS =
    [{
        Header: "Chart Name",
        accessor: "Chart Name",
        show: false,
        Filter: "",
    },
    {
        Header: "Chart Week",
        accessor: "Chart Week",
        Cell: ({ value }) => { return format(new Date(value), 'MMM d, Y') },
        show: true,
        Filter: ColumnFilter,
    },
    {
        Header: "",
        accessor: "Position",
        className: "number",
        Filter: "",
    },
    {
        Header: "Song Title",
        Filter: ColumnFilter,
        accessor: "Title",
        className: "title"
    },
    {
        Header: "Artist",
        Filter: ColumnFilter,
        accessor: "Artist",
        className: "artist"
    },
    {
        Header: "Song ID",
        Filter: ColumnFilter,
        accessor: "Song ID",
        show: false
    },
    {
        Header: "Spotify Streams",
        Filter: ColumnFilter,
        accessor: "Streams",
        className: "track-cell number",
        Cell: ({ value }) => {
            const disp = value > 0 ? value.toLocaleString() : '-'
            return disp
        }
    },
    {
        Header: "Billboard Weeks on Chart",
        Filter: ColumnFilter,
        accessor: "Weeks on Chart",
        className: "number",
        Cell: ({ value }) => {
            const disp = value > 0 ? value : '-'
            return disp
        }
    },
    {
        Header: "Billboard Peak Position",
        Filter: ColumnFilter,
        accessor: "Peak Position",
        className: "number",
        Cell: ({ value }) => {
            const disp = value > 0 ? value : '-'
            return disp
        }
    },
    {
        Header: "Billboard Last Position",
        Filter: ColumnFilter,
        accessor: "Last Position",
        className: "number",
        Cell: ({ value }) => {
            const disp = value > 0 ? value : '-'
            return disp
        }
    }]
