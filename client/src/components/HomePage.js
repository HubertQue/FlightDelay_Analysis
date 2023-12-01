import React from 'react'
import './home-page.css';
import airplane from '../../src/airplane.png'; // 确保路径正确


function HomePage() {
  return (
    <div className="home-page">
    <img src={airplane} alt="My Image" className="airplane_image" />
      <div class="container">
      <div class="block">the source of raw data </div>
      <div class="block">training data and relevant results </div>
      <div class="block">about deep learning to do some predictions</div>
    </div>

    </div>
  )
}

export default HomePage