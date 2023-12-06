import React from 'react';
import { Link } from 'react-router-dom'; 
import './home-page.css';
import airplane from '../../src/airplane.png';

function HomePage() {
  return (
    <div className="home-page">
      <div className="container">
        <Link to="/DataAnalysis" className="block">the source of raw data</Link>
        <Link to="/TrainingModels" className="block">training data and relevant results</Link>
        <Link to="/WeatherForm" className="block">about deep learning to do some predictions</Link>
      </div>
    </div>
  );
}

export default HomePage;