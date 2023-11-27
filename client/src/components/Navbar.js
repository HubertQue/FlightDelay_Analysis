import React from 'react'
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <div>
      <Link to="/HomePage">HomePage</Link>
      <Link to="/DataAnalysis">DataAnalysis</Link>
      <Link to="/TrainingModels">TrainingModels</Link>
      <Link to="/DeepLearning">DeepLearning</Link>
    </div>
  )
}

export default Navbar