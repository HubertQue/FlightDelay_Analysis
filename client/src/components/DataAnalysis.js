import React, { useState, useEffect } from 'react';
import './DataAnalysis.css'; 

const Sidebar = ({ onItemSelected }) => {
  return (
    <div className="sidebar">
      <button onClick={() => onItemSelected('GraphByTime')}>Time Graph</button>
      <button onClick={() => onItemSelected('GraphByLocation')}>Location Graph</button>
      <button onClick={() => onItemSelected('GraphByWeather')}>Weather Graph</button>
    </div>
  );
};

const SecondaryNavbar = ({ filters, onFilterSelected }) => {
  if (!filters) {
    return null; 
  }
  // console.log("filters: ", filters)
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

const Content = ({ selectedItem, allFilters, secondaryFilter}) => {
  return (
    <div className="content">
      {/* <SecondaryNavbar filters={allFilters} onFilterSelected={(filter) => console.log(filter)} /> */}
      <h2>Displaying content for {selectedItem} with filter: {secondaryFilter}</h2>
    </div>
  );
};

// 主组件
const DataAnalysis = () => {
  const [selectedItem, setSelectedItem] = useState('filter');
  const [secondaryFilter, setSecondaryFilter] = useState('');

  const allFiltersMap = {
    'GraphByTime': ['Graph By Year', 'Graph By month', 'Graph By Week'],
    'GraphByLocation': ['Graph By Country', 'Graph By State', 'Graph By City'],
    'GraphByWeather': ['Graph By Temperature', 'Graph By Precipitation']
  };

  // // 当selectedItem改变时，自动设置secondaryFilter为该项目的第一个次级选项
  // useEffect(() => {
  //   const filters = allFiltersMap[selectedItem];
  //   if (filters && filters.length > 0) {
  //     setSecondaryFilter(filters[0]); // 设置为第一个次级选项
  //   }
  // }, [selectedItem]); // 依赖数组中包含selectedItem，当它变化时触发效果


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