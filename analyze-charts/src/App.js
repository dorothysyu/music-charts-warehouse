import React, { useState, useEffect } from 'react'

const App = () => {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <p>data</p>
  )
}

export default App
