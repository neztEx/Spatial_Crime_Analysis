import React, { useCallback } from "react";
import {
  GoogleMap,
  useLoadScript,
  Marker,
  Circle,
  InfoWindow,
  Data,
  HeatmapLayer,
} from "@react-google-maps/api";
import usePlacesAutocomplete, {
  getGeocode,
  getLatLng,
} from "use-places-autocomplete";
import {
  Combobox,
  ComboboxInput,
  ComboboxPopover,
  ComboboxList,
  ComboboxOption,
} from "@reach/combobox";
import { formatRelative } from "date-fns";

import "@reach/combobox/styles.css";
// import mapStyles from "../mapStyles";
import "../App.css";
import * as QueryServer from './QueryServer'


const libraries = ["places", "visualization"];

const mapContainerStyle = {
  height: "70vh",
  width: "100vw",
};

// customize styles
const options = {
  // styles: mapStyles,
  disableDefaultUI: true,
  zoomControl: true,
  local: true
};

const center = {
  lat: 34.0522,
  lng: -118.2437,
};

export default function MapView() {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
    libraries,

  });

  const [selected, setSelected] = React.useState(null);

  const [crimeData, setCrimeData] = React.useState([])

  //we can retain state on 
  const mapRef = React.useRef()
  const onMapLoad = React.useCallback((map) => {
    mapRef.current = map
    console.log("LOADED MAP")
    QueryServer.location("LOS ANGELES").then(result_json => setCrimeData(result_json))
  }, [])

  const panTo = React.useCallback(({ lat, lng }) => {
    mapRef.current.panTo({ lat, lng })
    mapRef.current.setZoom(14)
  }, [])

  if (loadError) return "Error";
  if (!isLoaded) return "Loading...";

  return (
    <div>
      <Search panTo={panTo} />
      <Locate panTo={panTo} />

      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        zoom={11}
        center={center}
        options={options}
        onLoad={onMapLoad}
      >
        <HeatmapLayer data={HeatMap(crimeData)}/>
        {/* <DataPoints setSelected={setSelected} crimeData={crimeData} /> */}
        {/* <CrimeInfo selected={selected} setSelected={setSelected} /> */}

      </GoogleMap>
    </div>
  )
}

//Current Geolocation 
function Locate({ panTo }) {
  return <button className='locate' onClick={() => {
    navigator.geolocation.getCurrentPosition((position) => {
      console.log(position)
      panTo({
        lat: position.coords.latitude,
        lng: position.coords.longitude
      })
    })
  }}>
    <img src='compass.svg' alt='compass - locate me' />
  </button>
}

//Search bar
function Search({ panTo }) {

  const {
    ready,
    value,
    suggestions: { status, data },
    setValue,
    clearSuggestions } = usePlacesAutocomplete({
      requestOptions: {
        location: { lat: () => 34.0522, lng: () => -118.2437 },
        radius: 200 * 1000, // KM
      }
    })

  const handleInput = (e) => {
    setValue(e.target.value)
  }

  const handleSelect = async (address) => {
    setValue(address, false)
    clearSuggestions()
    try {
      const result = await getGeocode({ address })
      console.log(result[0])
      const { lat, lng } = await getLatLng(result[0])
      console.log(lat, lng)
      panTo({ lat, lng })
    } catch (error) {
      console.log("error!")
      console.log(error)
    }
  }


  return (
    <div className="search">
      <Combobox onSelect={handleSelect}>
        <ComboboxInput
          value={value}
          onChange={handleInput}
          disabled={!ready}
          placeholder="Enter Address"
        />
        <ComboboxPopover>
          <ComboboxList>
            {status === "OK" &&
              data.map(({ id, description }) => (
                <ComboboxOption key={id} value={description} />
              ))}
          </ComboboxList>
        </ComboboxPopover>
      </Combobox>
    </div>
  )
}

function DataPoints({ setSelected, crimeData }) {
  if (crimeData) {
    const points = crimeData.map((crime) =>
      <Circle
        key={crime.DR_NO}
        radius={100}
        center={{
          lat: crime.LAT,
          lng: crime.LON
        }}
        // icon={"https://storage.googleapis.com/support-kms-prod/SNP_2752125_en_v0"}
        // animation='BOUNCE'
        onClick={() => {
          setSelected(crime)
        }}
      />)

    return points
  }
  else return null
}

function HeatMap(crimeData) {
  if (crimeData) {
    const points = crimeData.map((crime) => { 
      return new window.google.maps.LatLng(crime.LAT, crime.LON)
    })
    return points
  }
  else return []
}

function CrimeInfo({ selected, setSelected }) {
  return (
    selected ? (
      <InfoWindow
        position={{ lat: selected.LAT, lng: selected.LON }}
        onCloseClick={() => {
          setSelected(null);
        }}
      >
        <div>
          <b>{selected.Crm_Cd_Desc}</b>
          <p>Details</p>
          <ul>
            <li>Age: {selected.Vict_Age}</li>
            <li>Sex: {selected.Vict_Sex}</li>
            <li>Time: {selected.TIME_OCC}</li>
          </ul>
        </div>
      </InfoWindow>
    ) : null
  )
}
