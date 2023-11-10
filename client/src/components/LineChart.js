import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

function LineChart() {

  const [data, setData] = useState({});

  useEffect(() => {
    fetch('http://localhost:5000/lineChartData')
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error fetching data: ', error));
  }, []);

  const inputs = {
    labels: data['label'],
    datasets: [
      {
        label: 'Attribute 1',
        data: data['attribute1'],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1  
      },
      {
        label: 'Attribute 2',
        data: data['attribute2'],
        fill: false,
        borderColor: 'rgba(255, 99, 132, 1)',
        tension: 0.1
      }
    ]
  };

  return(
    <div>
      {inputs && <Line data={inputs} />}
    </div>
  );
}

export default LineChart