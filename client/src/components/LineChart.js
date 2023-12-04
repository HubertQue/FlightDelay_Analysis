import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

function LineChart({props}) {

  const [data, setData] = useState({});

  useEffect(() => {
    fetch(`http://localhost:5000/lineChartData/${props}`)
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error fetching data: ', error));
  }, [props]);

  const inputs = {
    labels: data['label'],
    datasets: [
      {
        label: props + ` (X-axis: ${props}, Y-axis: Average Delay time)`,
        data: data['attribute2'],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1  
      }
    ],
  };

  return(
    <div>
      {inputs && <Line data={inputs} />}
    </div>
  );
}

export default LineChart