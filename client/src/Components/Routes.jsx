import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import Initialization from './Initialization'

const RoutesComponent = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/Initialization" element={<Initialization />} />
      </Routes>
    </Router>
  );
};

export default RoutesComponent;
