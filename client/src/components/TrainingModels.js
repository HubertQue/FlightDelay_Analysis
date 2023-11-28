import React from 'react'
import './TrainingModels.css'; 


function TrainingModels() {

  const modelResults = [
    { modelName: "Random Forest", accuracy: 0.7536, f1Score: 0.6906, precision: 0.0, recall: 0.0 },
    { modelName: "Model B", accuracy: 0.7716, f1Score: 0.6725, precision:0.0, recall: 0.0 },
    { modelName: "SVM", accuracy: 0.7716, f1Score: 0.6725, precision:0.0, recall: 0.0 },
  ];

  const ClassificationTable = ({ data }) => {
    return (
      <table >
        <thead>
          <tr>
            <th>Model Name</th>
            <th>Accuracy</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>F1 Score</th>
          </tr>
        </thead>
        <tbody>
          {data.map((model, index) => (
            <tr key={index}>
              <td>{model.modelName}</td>
              <td>{model.accuracy}</td>
              <td>{model.f1Score}</td>
              <td>{model.precision}</td>
              <td>{model.recall}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  
  return (
    <div className='TrainingModelsContainer'>
      <h1>Classification Matrix Table</h1>
      <ClassificationTable data={modelResults} />
    </div>
  )
}

export default TrainingModels