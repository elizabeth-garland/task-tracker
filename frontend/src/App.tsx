import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import axios from 'axios'
import './App.css'

function App() {

  // TODO: General app idea
  // - Basically just a way to track when you last did something and when you should do it again 

  // Fetch data from the backend
  const fetchData = async () => {
    try {
      const response = await axios.get('/api')
      console.log(response.data)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  };

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React dt</h1>
      <div className="card">
        <button onClick={() => fetchData()}>

        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to  HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App;
