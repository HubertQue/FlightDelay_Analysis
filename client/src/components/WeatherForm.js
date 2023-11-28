import React, { useState } from 'react';

function WeatherForm() {
  // 定义状态来存储输入值和结果
  const [date, setDate] = useState('');
  const [city, setCity] = useState('');
  const [temperature, setTemperature] = useState('');
  const [result, setResult] = useState(null);

  // 处理表单提交
  const handleSubmit = async (e) => {
    e.preventDefault();
  const data = { date, city, temperature };
  try {
    // 发送 POST 请求到后端
    const response = await fetch('https://your-backend-endpoint.com/submit-weather', {
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
          City Name:
          <input 
            type="text" 
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
        </label><br />

        <label>
          Temperature:
          <select 
            value={temperature}
            onChange={(e) => setTemperature(e.target.value)}
          >
            <option value="rain">Rain</option>
            <option value="sunny">Sunny</option>
            <option value="fog">Fog</option>
          </select>
        </label><br />

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
