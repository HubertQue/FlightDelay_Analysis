import React, { useState, useEffect } from 'react';
import './DataAnalysis.css'; 
import LineChart from './LineChart';
import BarChart from './BarChart';
import StateMap from './StateMap';

const Sidebar = ({ onItemSelected }) => {
  return (
    <div className="sidebar">
      <button onClick={() => onItemSelected('time')}>Analysis By Time</button>
      <button onClick={() => onItemSelected('geography')}>Analysis By Geography</button>
      <button onClick={() => onItemSelected('weather')}>Analysis By Weather</button>

    </div>
  );
};

const SecondaryNavbar = ({ filters, onFilterSelected }) => {
  if (!filters) {
    return null; 
  }
  return (
    <div className="secondary-navbar">
      {filters.map((filter) => (
        <button key={filter} onClick={() => onFilterSelected(filter)}>
          {filter}
        </button>
      ))}
    </div>
  );
};


const Content = ({ selectedItem, secondaryFilter}) => {
  const renderChart = () => {
    switch(secondaryFilter) {
      case "Year": 
        return <LineChart props="Year"/>;
      case "Month": 
        return <LineChart props="Month"/>;
      case "Week": 
        return <LineChart props="Week"/>;
      case "Hour": 
        return <LineChart props="Hour"/>;
      case "Country": 
        return <StateMap />;
      case "City": 
        return <></>;
      case "Elevation": 
        return <BarChart props="Elevation"/>;
      case "Temperature": 
        return <BarChart props="Temperature"/>;
      case "DEWP": 
        return <BarChart props="DEWP"/>;
      case "VISIB": 
        return ;
      case "WDSP": 
        return <BarChart props="WDSP"/>;
      case "PRCP": 
        return <BarChart props="PRCP"/>;
      case "SNDP": 
        return <BarChart props="SNDP"/>;
      case "FRSHTT": 
        return ;
      default:
        return <div>Click Tag</div>
    }
  }

  return (
    <div className="content">
      <h2>Displaying content for {selectedItem} with filter: {secondaryFilter}</h2>
      {renderChart()}
    </div>
  );
};

// 主组件
const DataAnalysis = () => {
  const [selectedItem, setSelectedItem] = useState('filter');
  const [secondaryFilter, setSecondaryFilter] = useState('');

  const allFiltersMap = {
    'time': ['Year', 'Month', 'Week', 'Hour'],
    'geography': ['Country', 'City'],
    'weather': ['Elevation', 'Temperature', 'DEWP', 'visibility', ' WDSP', 'PRCP','SNDP', 'FRSHTT']
  };


  useEffect(() => {
    const filters = allFiltersMap[selectedItem];
    if (filters && filters.length > 0) {
      setSecondaryFilter(filters[0]); // 
    }
  }, [selectedItem]); // 

  const allFilters = allFiltersMap[selectedItem];

  return (

    <div className="app-container">
      <Sidebar onItemSelected={(item) => {
        setSelectedItem(item);
        setSecondaryFilter(''); 
      }} />
      <div className="content-container">
        <SecondaryNavbar filters={allFilters} onFilterSelected={(filter) => setSecondaryFilter(filter)} />
        <Content
          selectedItem={selectedItem}
          secondaryFilter={secondaryFilter}
          allFilters={allFilters}
        />
      </div>
    </div>
  );
};

export default DataAnalysis;