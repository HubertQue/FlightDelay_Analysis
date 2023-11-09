import React, { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import 'chart.js/auto';

function PieChart() {
  const [chartData, setChartData] = useState({});

  useEffect(() => {
    fetch('http://localhost:5000/pieChartData')
      .then(response => response.json())
      .then(data => setChartData(data))
      .catch(error => console.error('Error fetching data: ', error));
  }, []);

  const inputs = {
    labels: chartData['label'],
    datasets: [
      {
        data: chartData['attribute'],
        backgroundColor: chartData['colors'], // 确保后端也提供了颜色数组
        borderColor: '#ffffff',
        borderWidth: 2,
      },
    ],
  };

  return (
    <div>
      {inputs && <Pie data={inputs} />}
    </div>
  );
}

export default PieChart;