import React from 'react'
import './css/DataIntro.css'; 


function DataIntro() {

  const DataTable1 = () => {
    const attributes = [
      { attribute: "Station", description: "Station number (WMO/DATSAV3 possibly combined w/WBAN number)" },
      { attribute: "DATE", description: "Given in mm/dd/yyyy format" },
      { attribute: "LATITUDE", description: "Given in decimated degrees (Southern Hemisphere values are negative)" },
      { attribute: "LONGITUDE", description: "Given in decimated degrees (Western Hemisphere values are negative)" },
      { attribute: "ELEVATION", description: "Given in meters" },
      { attribute: "NAME", description: "Name of station/airport/military base" },
      { attribute: "TEMP", description: "Mean temperature for the day in degrees Fahrenheit to tenths. " },
      { attribute: "DEWP", description: "Mean dew point for the day in degrees Fahrenheit to tenths. " },
      { attribute: "VISIB", description: "Mean visibility for the day in miles to tenths. " },
      { attribute: "WDSP", description: "Mean wind speed for the day in knots to tenths. " },
      { attribute: "MXSPD", description: "Maximum sustained wind speed reported for the day in knots to tenths. " },
      { attribute: "MAX", description: "Maximum temperature reported during the day in Fahrenheit to tenths. " },
      { attribute: "MIN", description: "Minimum temperature reported during the day in Fahrenheit to tenths. " },
      { attribute: "PRCP", description: "Total precipitation (rain and/or melted snow) reported during the day in inches and hundredths; will usually not end with the midnight observation (i.e. may include latter part of previous day). “0” indicates no measurable precipitation (includes a trace). " },
      { attribute: "SNDP", description: "Snow depth in inches to tenths. It is the last report for the day if reported more than once. " },
      { attribute: "FRSHTT", description: "FRSHTT - Indicators (1 = yes, 0 = no/not reported) for the occurrence during the day of: Fog ('F' - 1st digit). Rain or Drizzle ('R' - 2nd digit).Snow or Ice Pellets ('S' - 3rd digit).Hail ('H' - 4th digit).Thunder ('T' - 5th digit).Tornado or Funnel Cloud ('T' - 6th digit)." }
    ];
  
    return (
      <table>
        <thead>
          <tr>
            <th>Attribute</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {attributes.map((item, index) => (
            <tr key={index}>
              <td>{item.attribute}</td>
              <td>{item.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const DataTable2 = () => {
    const attributes = [
      { attribute: "YEAR", description: "Year" },
      { attribute: "FL_DATE", description: "Flight Date (yyyymmdd)" },
      { attribute: "ORIGIN", description: "Origin Airport" },
      { attribute: "ORIGIN_STATE_NM", description: "Origin Airport, State Name" },
      { attribute: "DEST_CITY_NAME", description: "Destination Airport, City Name" },
      { attribute: "DEST_STATE_NM", description: "Destination Airport, State Name" },
      { attribute: "DEP_TIME", description: "Actual Departure Time (local time: hhmm)" },
      { attribute: "DEP_DELAY", description: "Difference in minutes between scheduled and actual departure time. Early departures show negative numbers" },
      { attribute: "CANCELLED", description: "Cancelled Flight Indicator (1=Yes)" }
    ];
  
    return (
      <table>
        <thead>
          <tr>
            <th>Attribute</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {attributes.map((item, index) => (
            <tr key={index}>
              <td>{item.attribute}</td>
              <td>{item.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  
  return (
    <div className='TrainingModelsContainer'>
      <h1>Introduction</h1>
      <div style={{paddingTop:'0px', paddingBottom:'0px'}}>Inspired by the Kaggle dataset&nbsp;            
        <a href="https://www.kaggle.com/datasets/threnjen/2019-airline-delays-and-cancellations" target="_blank" rel="noopener noreferrer">
          https://www.kaggle.com/datasets/threnjen/2019-airline-delays-and-cancellations
        </a>
        , our group decided to further 
        investigate the relationship between airport weather conditions and flight delays/cancellations. Noticed that this Kaggle dataset is made by joining 
        two public datasets from where limited attribute are included and only data in 2019 was used. From the source datasets, we found that the source dataset 
        contains a wealth of relevant attributes, which has rich potential that we can do more research by using more attributes and expanding the target year 
        from a single year to several years.
      </div>
      <h2>Below are the links of our two raw datasets and the tables of attributes</h2>
      <h1>
        <a href="https://www.ncei.noaa.gov/access/search/data-search/global-summary-of-the-day" target="_blank" rel="noopener noreferrer">
          Weather Dataset   
        </a> 
        
      </h1>
      <h3><p><i>From National Centers for Environmental Information (NOAA)</i></p></h3>
      <DataTable1 />
      <h1>
        <a href="https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FGK" target="_blank" rel="noopener noreferrer">
          Flight Status Dataset
        </a>
      </h1>
      <h3><p><i>From Bureau of Transportation statistics</i></p></h3>
      <DataTable2 />
    </div>
  )
}

export default DataIntro