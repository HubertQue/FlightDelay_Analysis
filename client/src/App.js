import React from 'react';
// import LineChart from './components/LineChart';
// import PieChart from './components/PieChart';
import { BrowserRouter, Route, Routes } from "react-router-dom";

import Navbar from './components/Navbar';

import TrainingModels from './components/TrainingModels';
import DataAnalysis from './components/DataAnalysis';
import DeepLearning from './components/DeepLearning';
import HomePage from './components/HomePage';

function App() {
 
  return (
    <div>
      <BrowserRouter>
        <Navbar />
        
        <Routes>
          <Route path="/HomePage" element={<HomePage />} />
          <Route path="/DataAnalysis" element={<DataAnalysis />} />
          <Route path="/TrainingModels" element={<TrainingModels />} />
          <Route path="/DeepLearning" element={<DeepLearning />} />
        </Routes>
          
      </BrowserRouter>

    </div>
  );
}

export default App;