import React from 'react'
import '../App.css'
import MapView from '../components/GoogleMap';
import Switch from "react-switch";


function Visualizations() {
  const [heatMap, setheatMap] = React.useState(false);
  return (
        <div>
          <MapView heatMap={heatMap} />
          <Switch onChange={(checked)=> {setheatMap(checked)}} checked={heatMap}/>
        </div>
        
    )
}

export default Visualizations;
