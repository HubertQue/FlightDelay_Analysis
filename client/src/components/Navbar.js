import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../../src/static/airplane_icon.png';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';

function Navbar() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static"> 
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
          </IconButton>
          <img src={logo} alt="Logo" style={{ marginRight: '20px', width: '50px', height: '50px' }} />
          <Button color="inherit" component={Link} to="/" sx={{ fontSize: '1rem', marginLeft:20, marginRight: 20 }}>Home Page</Button>
          <Button color="inherit" component={Link} to="/DataAnalysis" sx={{ fontSize: '1rem',marginRight: 20 }}>Data Analysis</Button>
          <Button color="inherit" component={Link} to="/TrainingModels" sx={{ fontSize: '1rem',marginRight: 20 }}>Models</Button>
          <Button color="inherit" component={Link} to="/WeatherForm" sx={{ fontSize: '1rem',marginRight: 10 }}>Weather Form</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default Navbar;