import React, { useState, useEffect } from 'react';
import './css/DataAnalysis.css'; 
import LineChart from './LineChart';
import BarChart from './BarChart';
import StateMap from './StateMap';

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import TimelineIcon from '@mui/icons-material/Timeline';
import LandscapeIcon from '@mui/icons-material/Landscape';
import WeatherIcon from '@mui/icons-material/WbSunny'; 


const Sidebar = ({ onItemSelected }) => {
  return (
    <Box
      sx={{
        width: 280,
        bgcolor: '#222D32', 
        color: 'white', 
        '& .MuiListItemIcon-root': {
          color: 'white', 
        },
        '& .MuiListItemText-primary': { 
          color: 'white', 
        }
      }}
    >
      <List>
        <ListItem button onClick={() => onItemSelected('time')}>
          <ListItemIcon>
            <TimelineIcon />
          </ListItemIcon>
          <ListItemText primary="Analysis By Time" />
        </ListItem>
        <ListItem button onClick={() => onItemSelected('geography')}>
          <ListItemIcon>
            <LandscapeIcon />
          </ListItemIcon>
          <ListItemText primary="Analysis By Geography" />
        </ListItem>
        <ListItem button onClick={() => onItemSelected('weather')}>
          <ListItemIcon>
            <WeatherIcon />
          </ListItemIcon>
          <ListItemText primary="Analysis By Weather" />
        </ListItem>
      </List>
    </Box>
  );
};

const SecondaryNavbar = ({ filters, onFilterSelected, selectedFilter }) => {
  if (!filters) {
    return null;
  }


  function switchFilter(filter) {
    switch (filter) {
      case 'Year':
        return 'Year';
      case 'Month':
        return 'Month';
      case 'Week':
        return 'Week';
      case 'Hour':
        return 'Hour';
      case 'Country':
        return 'Country';
      case 'City':
        return 'City';
      case 'Elevation':
        return 'Elevation';
      case 'Temperature':
        return 'Temperature';
      case 'DEWP':
        return 'Dew point';
      case 'VISIBILITY':
        return 'VISIBILITY';
      case 'WDSP':
        return 'Wind speed';
      case 'PRCP':
        return 'Precipitation ';
      case 'SNDP':
        return 'Snow depth';
      case 'FRSHTT':
        return 'Weather Condition';
      default:
        return "default"
    }
  }

  return (
    <div className="secondary-navbar" >
      {filters.map((filter) => (
        <Button
          key={filter}
          onClick={() => onFilterSelected(filter)}
          variant="outlined"
          style={{
            margin: '0 8px', // 设置按钮间距
            color: selectedFilter === filter ? 'darkslategray' : 'white', // 选中的按钮用深色文字，未选中的用白色文字
            borderColor: 'white', // 边框颜色设置为白色
            backgroundColor: selectedFilter === filter ? 'white' : 'transparent' // 选中的按钮背景为白色
          }}
        >
          {switchFilter(filter)}
        </Button>
      ))}
    </div>
  );
};

const Content = ({ selectedItem, secondaryFilter}) => { 
  console.log(secondaryFilter)
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
      case "Elevation": 
        return <BarChart props="Elevation"/>;
      case "Temperature": 
        return <BarChart props="Temperature"/>;
      case "DEWP": 
        return <BarChart props="DEWP"/>;
      case "WDSP": 
        return <BarChart props="WDSP"/>;  
      case "PRCP": 
        return <BarChart props="PRCP"/>;
      case "SNDP": 
        return <BarChart props="SNDP"/>;
      case "FRSHTT": 
        return <BarChart props="FRSHTT"/>;;
      default:
        return <div>Please Click the Top Tag</div>
    }
  }

  return (
    <div className="content">
      {/* <h2>Displaying content for {selectedItem} with filter: {secondaryFilter}</h2> */}
      {renderChart()}
    </div>
  );
};

// 主组件
const DataAnalysis = () => {
  const [selectedItem, setSelectedItem] = useState('time');
  const [secondaryFilter, setSecondaryFilter] = useState('');

  const allFiltersMap = {
    'time': ['Year', 'Month', 'Week', 'Hour'],
    'geography': ['Country'],
    'weather': ['Elevation', 'Temperature', 'DEWP', 'WDSP', 'PRCP','SNDP', 'FRSHTT']
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
        if (item !== selectedItem) {
          // 只有当选择的项目改变时才更新 secondaryFilter
          const firstFilter = allFiltersMap[item] && allFiltersMap[item][0];
          setSecondaryFilter(firstFilter || ''); 
        }
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