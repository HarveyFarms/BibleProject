import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import WelcomePage from './Pages/Welcome';
import ExampleData from './Pages/ExampleData';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Routes>
        {/* Redirect logic AFTER loading */}
        <Route path="/" element={<WelcomePage />} />
        <Route path="/example-data" element={<ExampleData />} />
      </Routes>
    </>
  )
}

export default App
