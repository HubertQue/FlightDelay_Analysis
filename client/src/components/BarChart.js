import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

function BarChart({ props }) { // 假设你传递的是一个endpoint参数

  const [chartData, setChartData] = useState({});

  useEffect(() => {
    fetch(`http://localhost:5000/barChartData/${props}`)
      .then(response => response.json())
      .then(data => setChartData(data))
      .catch(error => console.error('Error fetching data: ', error));
  }, [props]);

  const options = {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  const data = {
    labels: chartData['label'], 
    datasets: [
      {
        label: props,
        data: chartData['data'], 
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      }
    ]
  };

  const data2 = {
    labels: chartData['label'], 
    datasets: [
      {
        label: 'Without',
        data: chartData['data'], 
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
      {
        label: 'With',
        data: chartData['data1'], 
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      }
    ]
  };

  const inputData = props === 'FRSHTT' ? data2 : data;

  return (

    <div>
      <Bar data={inputData} options={options} />
    </div>
  );
}

export default BarChart;