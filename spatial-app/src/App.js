import './App.css';
import Navbar from './components/navbar.js';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './pages/Home.js';
import Analytics from './pages/Analytics.js';
import Visualizations from './pages/Visualizations.js';
import React from 'react'

function App() {
  return (
    <>
        <BrowserRouter>
          <Navbar/>
          <Routes>
            <Route path='/' element={<Home/>} />
            <Route path='/overview' element={<Analytics/>} />
            <Route path='/map' element={<Visualizations/>} />
            
          </Routes>
        </BrowserRouter>
    </>
  );
}

export default App;