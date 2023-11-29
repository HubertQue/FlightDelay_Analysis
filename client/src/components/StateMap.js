import React from "react";
import MapChart from "./MapChart";

const StateMap = () => {

  const data = [];

  for (let i = 1; i <= 51; i++) {
    data.push({
      id: i.toString().padStart(2, '0'), // 确保id总是两位数
      value: i
    });
  } 

  return (
    <div>
      <MapChart data={data} />
    </div>
  );
};

export default StateMap;