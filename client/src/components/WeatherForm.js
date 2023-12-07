import React, { useState } from 'react';
import { TextField, Button, FormControl, InputLabel, Select, MenuItem, Checkbox, FormControlLabel, Dialog, DialogTitle, DialogContent, Typography  } from '@mui/material';
import './css/WeatherForm.css'; 


function WeatherForm() {
  // 定义状态来存储输入值和结果
  const [date, setDate] = useState('');
  const [hour, setHour] = useState('');
  const [airport, setAirport] = useState('');
  const [AveT, setAveT] = useState('');
  const [MaxT, setMaxT] = useState('');
  const [MinT, setMinT] = useState('');
  const [visibility, setVisibility] = useState('high');
  // const [weatherCondition, setWeatherCondition] = useState('');
  const [result, setResult] = useState(null);

  // 处理表单提交
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!date.trim()) {
      alert("Please enter the date."); 
      return; 
    }
    if (!hour.trim()) {
      alert("Please enter the hour."); 
      return; 
    }
    if (!airport.trim()) {
      alert("Please enter the airport."); 
      return; 
    }
    if (!AveT.trim()) {
      alert("Please enter the average temperature."); 
      return; 
    }
    if (!MaxT.trim()) {
      alert("Please enter the maximum temperature."); 
      return; 
    }
    if (!MinT.trim()) {
      alert("Please enter the minimum temperature."); 
      return; 
    }


    const data = { date, hour, airport, AveT, MaxT, MinT, visibility, weatherConditions };
    try {
      // 发送 POST 请求到后端
      const response = await fetch('http://localhost:5000/weatherform', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // 获取并处理来自后端的响应
      const responseData = await response.json();
      let responseMessage;
      if (responseData['pred'] === '0') {
        responseMessage = `The Expected Delay is 0-15 minutes. (Prediction confidence: ${(responseData['prob'] * 100).toFixed(2)}%)`;
      } else if (responseData['pred'] === '1') {
        responseMessage = `The Expected Delay is >15 minutes. (Prediction confidence: ${(responseData['prob'] * 100).toFixed(2)}%)`;
      } else {
        responseMessage = `Unknown airport code received. Please provide a valid code. ${responseData['pred']}`;
      }
  
      setResult(responseMessage);
      showDialog();
    } catch (error) {
      console.error('Error during data submission:', error);
      setResult('Failed to submit data.');
      showDialog();
    }
  };


const [weatherConditions, setWeatherConditions] = useState({
  Fog: false,
  Rain: false,
  Snow: false,
  Hail: false,
  Thunder: false,
  Tornado: false,
  None: false
});

const handleCheckboxChange = (event) => {
  
  const { name, checked } = event.target;

  if (name === 'None') {
    // 如果选择了 "None"，清除其他所有选项
    setWeatherConditions({
      Fog: false,
      Rain: false,
      Snow: false,
      Hail: false,
      Thunder: false,
      Tornado: false,
      None: checked
    });
  } else {
    // 如果选择了其他选项，则确保 "None" 不被选中
    setWeatherConditions({
      ...weatherConditions,
      [name]: checked,
      None: false
    });
  }
};

// 新增一个状态来控制弹窗的打开和关闭
const [openDialog, setOpenDialog] = useState(false);

// 当表单提交成功或失败时，打开弹窗
const showDialog = () => {
  setOpenDialog(true);
};

// 关闭弹窗的函数
const handleCloseDialog = () => {
  setOpenDialog(false);
};

   
return (
  <div className="formContainer" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '110vh', flexDirection: 'column'  }}>
    <Typography variant="h6" style={{ marginBottom: '20px' }}>
        Enter The Below Information To Predict Your Flight Delay
    </Typography>
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', width: '50%' }}>
      <TextField
        label="Date"
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        margin="normal"
        InputLabelProps={{
          shrink: true, 
        }}
      />
      <TextField
        label="Current Hour"
        type="text"
        value={hour}
        onChange={(e) => setHour(e.target.value)}
        margin="normal"
        InputLabelProps={{
          shrink: true, 
        }}
        placeholder="e.g. 0-23"
      />
      <TextField
        label="IATA Airport Code"
        type="text"
        value={airport}
        onChange={(e) => setAirport(e.target.value)}
        margin="normal"
        InputLabelProps={{
          shrink: true, 
        }}
        placeholder="e.g. LAX or PHX or HDN"
      />
      <TextField
        label="Average Temperature"
        type="text"
        value={AveT}
        onChange={(e) => setAveT(e.target.value)}
        margin="normal"
        InputLabelProps={{
          shrink: true, 
        }}
        placeholder="e.g. 50.0"
      />
      <TextField
        label="Max Temperature"
        type="text"
        value={MaxT}
        onChange={(e) => setMaxT(e.target.value)}
        margin="normal"
        InputLabelProps={{
          shrink: true, 
        }}
        placeholder="e.g. 70.0"
      />
      <TextField
        label="Min Temperature"
        type="text"
        value={MinT}
        onChange={(e) => setMinT(e.target.value)}
        margin="normal"
        InputLabelProps={{
          shrink: true, 
        }}
        placeholder="e.g. 40.0"
      />

      <FormControl margin="normal">
        <InputLabel>Visibility</InputLabel>
        <Select
          value={visibility}
          onChange={(e) => setVisibility(e.target.value)}
        >
          <MenuItem value="high">High Visibility (&gt;1 miles)</MenuItem>
          <MenuItem value="medium">Medium Visibility (0.4-1 miles)</MenuItem>
          <MenuItem value="low">Low Visibility (0-0.4 miles)</MenuItem>
          
          
        </Select>
      </FormControl>

      <div>
        <FormControlLabel
          control={<Checkbox checked={weatherConditions.Fog} onChange={handleCheckboxChange} name="Fog" />}
          label="Fog"
        />
        <FormControlLabel
          control={<Checkbox checked={weatherConditions.Rain} onChange={handleCheckboxChange} name="Rain" />}
          label="Rain or Drizzle  "
        />
        <FormControlLabel
          control={<Checkbox checked={weatherConditions.Snow} onChange={handleCheckboxChange} name="Snow" />}
          label="Snow or Ice Pellets"
        />
        <FormControlLabel
          control={<Checkbox checked={weatherConditions.Hail} onChange={handleCheckboxChange} name="Hail" />}
          label="Hail"
        />
        <FormControlLabel
          control={<Checkbox checked={weatherConditions.Thunder} onChange={handleCheckboxChange} name="Thunder" />}
          label="Thunder"
        />
        <FormControlLabel
          control={<Checkbox checked={weatherConditions.Tornado} onChange={handleCheckboxChange} name="Tornado" />}
          label="Tornado or Funnel Cloud"
        />
        
      </div>

      <Button type="submit" variant="contained" color="primary" style={{ marginTop: '20px' }}>
        Start Predict
      </Button>
    </form>

    <Dialog open={openDialog} onClose={handleCloseDialog}>
      <DialogTitle>Prediction Result:</DialogTitle>
      <DialogContent>
        {result}
      </DialogContent>
    </Dialog>
  </div>
);
}

export default WeatherForm;
