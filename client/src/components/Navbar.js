import React from 'react'
import { Link } from 'react-router-dom';
import './Navbar.css';
import logo from '../../src/sfu_logo.png';

function Navbar() {
  return (
    <div className="navbar-container">

      <Link to="/HomePage">HomePage</Link>
      <Link to="/DataAnalysis">DataAnalysis</Link>
      <Link to="/TrainingModels">TrainingModels</Link>
      <Link to="/DeepLearning">DeepLearning</Link>
      <img src={logo} alt="Logo" className="navbar-logo" /> {/* 添加图片并赋予类名 */}

    </div>
  )
}

export default Navbar