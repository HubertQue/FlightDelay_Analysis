import React from 'react';
import MapChart from "./MapChart";
import Typography from '@mui/material/Typography';

const StateMap = () => {


  const data = [{'key': 'Texas', 'value': 33.42}, {'key': 'California', 'value': 31.95}, {'key': 'Florida', 'value': 34.27}, {'key': 'Illinois', 'value': 34.21}, {'key': 'Georgia', 'value': 29.06}, {'key': 'North Carolina', 'value': 36.22}, {'key': 'Washington', 'value': 26.9}, {'key': 'New York', 'value': 42.3}, {'key': 'Arizona', 'value': 28.36}, {'key': 'Nevada', 'value': 26.66}, {'key': 'Virginia', 'value': 47.04}, {'key': 'Michigan', 'value': 40.71}, {'key': 'Utah', 'value': 30.88}, {'key': 'Pennsylvania', 'value': 44.52}, {'key': 'Maryland', 'value': 23.08}, {'key': 'New Jersey', 'value': 40.23}, {'key': 'Tennessee', 'value': 34.53}, {'key': 'Minnesota', 'value': 36.99}, {'key': 'Missouri', 'value': 33.37}, {'key': 'Massachusetts', 'value': 35.36}, {'key': 'Hawaii', 'value': 26.69}, {'key': 'Ohio', 'value': 43.66}, {'key': 'Oregon', 'value': 34.32}, {'key': 'Louisiana', 'value': 40.14}, {'key': 'Kentucky', 'value': 46.75}, {'key': 'Indiana', 'value': 41.89}, {'key': 'Wisconsin', 'value': 49.4}, {'key': 'South Carolina', 'value': 48.36}, {'key': 'Puerto Rico', 'value': 39.84}, {'key': 'Alaska', 'value': 29.99}, {'key': 'Oklahoma', 'value': 43.92}, {'key': 'Montana', 'value': 50.56}, {'key': 'Colorado', 'value': 76.37}, {'key': 'Alabama', 'value': 48.22}, {'key': 'Idaho', 'value': 48.65}, {'key': 'Iowa', 'value': 52.46}, {'key': 'Arkansas', 'value': 47.86}, {'key': 'Nebraska', 'value': 50.54}, {'key': 'New Mexico', 'value': 41.39}, {'key': 'Connecticut', 'value': 43.77}, {'key': 'North Dakota', 'value': 69.13}, {'key': 'South Dakota', 'value': 59.36}, {'key': 'Rhode Island', 'value': 40.75}, {'key': 'Mississippi', 'value': 52.15}, {'key': 'Maine', 'value': 59.65}, {'key': 'Kansas', 'value': 58.01}, {'key': 'West Virginia', 'value': 62.62}, {'key': 'Vermont', 'value': 66.29}, {'key': 'New Hampshire', 'value': 49.67}, {'key': 'Wyoming', 'value': 80.41}, {'key': 'U.S. Pacific Trust Territories and Possessions', 'value': 49.09}]

  return (
    <div>
      <Typography variant="subtitle1" align="center" style={{ margin: '20px' }}>
        <b>Each state's number represents the Average Delay Time in minutes. Darker colors indicate higher values, while lighter colors indicate lower values.</b>
      </Typography>
      <MapChart data={data} />
    </div>
  );
};

export default StateMap;