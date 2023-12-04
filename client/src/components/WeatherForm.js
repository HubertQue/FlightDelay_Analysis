import React, { useState } from 'react';

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
      console.log(responseData); // 或者做其他处理
      setResult(`Received response: ${JSON.stringify(responseData)}`);

    } catch (error) {
      console.error('Error during data submission:', error);
      setResult('Failed to submit data.');
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
   
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Date:
          <input 
            type="date" 
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </label><br />

        <label>
          Current Hour:
          <input 
            type="text" 
            value={hour}
            onChange={(e) => setHour(e.target.value)}
          />
        </label>
        <span>(e.g. 0-24)</span>
        <br />

        <label>
          Airport:
          <input 
            type="text" 
            value={airport}
            onChange={(e) => setAirport(e.target.value)}
          />
        </label>
        <span>(e.g. LAX)</span>
        <br />

        <label>
          Average Temperature:
          <input 
            type="text" 
            value={AveT}
            onChange={(e) => setAveT(e.target.value)}
          />
        </label>
        <span>(eg: 70)</span>
        <br />
        <label>
          Max Temperature:
          <input 
            type="text" 
            value={MaxT}
            onChange={(e) => setMaxT(e.target.value)}
          />
        </label>
        <span>(eg: 80)</span>
        <br />
        <label>
          Min Temperature:
          <input 
            type="text" 
            value={MinT}
            onChange={(e) => setMinT(e.target.value)}
          />
        </label>
        <span>(eg: 50)</span>
        <br />

        <label>
          Visibility:
          <select 
            value={visibility}
            onChange={(e) => setVisibility(e.target.value)}
          >
            <option value="low">Low Visibility <span>(0-0.4 miles)</span></option>
            <option value="medium">Medium Visibility <span>(0.4-1 miles)</span></option>
            <option value="high">High Visibility <span>(&gt;1 miles)</span></option>
          </select>
        </label><br />
        
        <div>
          Weather Condition:
        </div>

        <div>
        <label>
          <input 
            type="checkbox" 
            name="Fog" 
            checked={weatherConditions.Fog} 
            onChange={handleCheckboxChange} 
          />
          Fog
        </label>

        <label>
          <input 
            type="checkbox" 
            name="Rain" 
            checked={weatherConditions.Rain} 
            onChange={handleCheckboxChange} 
          />
          Rain or Drizzle
        </label>

        <label>
          <input 
            type="checkbox" 
            name="Snow" 
            checked={weatherConditions.Snow} 
            onChange={handleCheckboxChange} 
          />
          Snow or Ice Pellets
        </label>

        <label>
          <input 
            type="checkbox" 
            name="Hail" 
            checked={weatherConditions.Hail} 
            onChange={handleCheckboxChange} 
          />
          Hail
        </label>

        <label>
          <input 
            type="checkbox" 
            name="Thunder" 
            checked={weatherConditions.Thunder} 
            onChange={handleCheckboxChange} 
          />
          Thunder
        </label>

        <label>
          <input 
            type="checkbox" 
            name="Tornado" 
            checked={weatherConditions.Tornado} 
            onChange={handleCheckboxChange} 
          />
          Tornado or Funnel Cloud
        </label>

        <label>
          <input 
            type="checkbox" 
            name="None" 
            checked={weatherConditions.None} 
            onChange={handleCheckboxChange} 
          />
          None
        </label>
      </div>


        <button type="submit">Submit</button>
      </form>

      {result && (
        <div className="result">
          {result}
        </div>
      )}
    </div>
  );
}

export default WeatherForm;
