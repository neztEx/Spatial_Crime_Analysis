import React from 'react';
import logo from '../logo.svg';
import '../App.css';
import EsriLoaderReact from 'esri-loader-react';

function MapView(){

    const options = {
      url: 'https://js.arcgis.com/4.6/'
    };

    return (
      <div className="App">
        {/* <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p> */}
        <EsriLoaderReact 
          options={options} 
          modulesToLoad={['esri/Map', 'esri/views/MapView']}    
          onReady={({loadedModules: [Map, MapView], containerNode}) => {
            new MapView({
              container: containerNode,
              map: new Map({basemap: 'topo'}),
              zoom: 11, // Sets zoom level based on level of detail (LOD)
              center: [-118.2437, 34.05] // Sets center point of view using longitude,latitude
            })
          }}
        />
      </div>
    );
}

export default MapView;
