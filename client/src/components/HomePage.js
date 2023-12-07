import React from 'react';
import { Link } from 'react-router-dom'; 
import './home-page.css';

function HomePage() {
  return (
    <div className="home-page">
      <div className="container">
        <Link to="/DataAnalysis" className="block">View the source of raw data</Link>
        <Link to="/TrainingModels" className="block">View the training results</Link>
        <Link to="/WeatherForm" className="block">Start Prediction for you Flight</Link>
      </div>
    </div>
  );
}

export default HomePage;