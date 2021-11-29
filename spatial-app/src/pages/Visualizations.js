import React from 'react'
import '../App.css'
import MapView from '../components/GoogleMap';
import Switch from "react-switch";

import * as QueryServer from '../components/QueryServer'


function Visualizations() {
  const [heatMap, setheatMap] = React.useState(false);

  const [crimeData, setCrimeData] = React.useState([])

  const [queryType, setQueryType] = React.useState("location");

  const [queryUpdated, setQueryUpdated] = React.useState(false);

  const options = [
    {value: 'location', label: 'Location' }
  ]

  const onSelectChange = React.useEffect(() => {
    setQueryUpdated(!queryUpdated);
  }, [queryType])

  const onQueryChange = React.useEffect(() => {
    switch(queryType){
      case 'location':
        QueryServer.location("LOS ANGELES").then(result_json => setCrimeData(result_json))
        break;
      default:
        QueryServer.location("LOS ANGELES").then(result_json => setCrimeData(result_json))
    }
  }, [queryUpdated])

  const handleChange = (selectedOption) => {
    setQueryType(selectedOption);
  }

  return (
        <div>
          <MapView heatMap={heatMap} crimeData={crimeData}/>
          <Switch onChange={(checked)=> {setheatMap(checked)}} checked={heatMap}/>
        </div>
        
    )
}

export default Visualizations;
