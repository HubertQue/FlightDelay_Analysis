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

  const options = {
    scales: {
      x: {
        title: {
          display: true,
          text: props,
          font: {
            size: 15,
          }
        }
      },
      y: {
        title: {
          display: true,
          text: 'Average Delay Time (minutes)',
          font: {
            size: 15,
          }
        }
      }
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
      }
    },
  };

  const inputs = {
    labels: data['label'],
    datasets: [
      {
        label: props + " in 2020 ",
        data: data['attribute2'],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1  
      },
      {
        label: props + " in 2021 ",
        data: data['attribute3'],
        fill: false,
        borderColor: 'red',
        tension: 0.1  
      },
      {
        label: props + " in 2022 ",
        data: data['attribute4'],
        fill: false,
        borderColor: 'green',
        tension: 0.1  
      }
    ],
    
  };

  return(
    <div>
      {inputs && <Line data={inputs} options={options}/>}
    </div>
  );
}

export default LineChart