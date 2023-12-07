import React from 'react';
import { Link } from 'react-router-dom'; 
import './css/HomePage.css';

function HomePage() {
  return (
    <div className="home-page">
      <div className="container">
        <Link to="/DataIntro" className="block">Explore Raw Data Sources</Link>
        <Link to="/DataAnalysis" className="block">View Data Analysis Outcomes</Link>
        <Link to="/WeatherForm" className="block">Start Prediction for Flights</Link>
      </div>
    </div>
  );
}

export default HomePage;