import React, { useState } from "react";
import * as d3 from "d3";
import { ComposableMap, Geographies, Geography } from "react-simple-maps";

const MapChart = ({ data }) => {
  const [tooltipContent, setTooltipContent] = useState('');
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const geoUrl = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json";

  // 定义颜色比例尺
  const colorScale = d3.scaleLinear()
                       .domain([Math.min(...data.map(item => item.value)), Math.max(...data.map(item => item.value))])
                       .range(["#ffedea", "#ff5233"]);
  console.log(Math.max(...data.map(item => item.value)))
  // 鼠标悬停事件处理函数
  const handleMouseEnter = (geo, cur, event) => {
    // 获取鼠标位置和地图容器的偏移量
    const { clientX, clientY } = event;
    const xOffset = 20; // 横向偏移量
    const yOffset = -40; // 纵向偏移量
  
    // 地图容器的偏移量
    const mapContainer = event.target.closest("div");
  
    // 考虑地图容器的偏移量和页面滚动量
    const x = clientX - mapContainer.getBoundingClientRect().left + window.scrollX + xOffset;
    const y = clientY - mapContainer.getBoundingClientRect().top + window.scrollY + yOffset;
  
    const content = cur ? `${geo.properties.name}: ${cur.value}` : 'No data';
    setTooltipContent(content);
    setTooltipPosition({ x, y });
  };

  // 鼠标离开事件处理函数
  const handleMouseLeave = () => {
    setTooltipContent('');
    setTooltipPosition({ x: 0, y: 0 });
  };

  return (
    <div style={{ position: 'relative' }}>
      {tooltipContent && (
        <div style={{
          position: 'absolute',
          left: `${tooltipPosition.x}px`,
          top: `${tooltipPosition.y}px`,
          padding: '5px',
          background: 'white',
          border: 'solid 1px #DDD',
          pointerEvents: 'none',
          zIndex: 1000
        }}>
          {tooltipContent}
        </div>
      )}
      <ComposableMap 
        projection="geoAlbersUsa"
      projectionConfig={{
        scale: 800,
        translate: [487.5, 305]
      }}
      style={{
        width: "975px",
        height: "610px"
      }}
      >
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map(geo => {
              // console.log(geo.properties.name)
              // console.log(data[0])
              const cur = data.find(s => s.key === geo.properties.name);
              return (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  fill={cur ? colorScale(cur.value) : "#EEE"}
                  onMouseEnter={(event) => handleMouseEnter(geo, cur, event)}
                  onMouseMove={(event) => handleMouseEnter(geo, cur, event)}
                  onMouseLeave={handleMouseLeave}
                  style={{
                    
                    pressed: {
                      outline: 'none'
                    }
                  }}
                />
              );
            })
          }
        </Geographies>
      </ComposableMap>
    </div>
  );
};

export default MapChart;