import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

function BarChart({ props }) { 

  const [chartData, setChartData] = useState({});

  useEffect(() => {
    fetch(`http://localhost:5000/barChartData/${props}`)
      .then(response => response.json())
      .then(data => setChartData(data))
      .catch(error => console.error('Error fetch data: ', error));
  }, [props]);

  const getXAxisTitle = (prop) => {
    console.log(props)
    switch (prop) {
      case 'Elevation':
        return 'Elevation (Meters)';
      case 'Temperature':
        return 'Temperature (Centigrade)';
      case 'DEWP':
        return 'Dew Point (Fahrenheit)';
      case 'WDSP':
        return 'Wind Speed (Knots)';
      case 'PRCP':
        return 'Precipitation (Inches)';
      case 'SNDP':
        return 'Snow Depth (Inches)';
      case 'FRSHTT':
        return 'Extreme Weather';
      default:
        return 'Default X Axis Title';
    }
  };

  const xAxisTitle = getXAxisTitle(props);

  const options = {
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Average Delay Time (minutes)', 
          font: {
            size: 15 
          }
        }
      },
      x: {
        title: {
          display: true,
          text: xAxisTitle,
          font: {
            size: 15,
          }
        }
      }
    }
  };

  const data = {
    labels: chartData['label'], 
    datasets: [
      {
        label: props,
        data: chartData['data'], 
        //backgroundColor: ['rgba(255, 99, 132, 0.5)'],
        //borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
        barPercentage: 0.8,
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