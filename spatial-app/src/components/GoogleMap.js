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


const libraries = ["places", "visualization"];

const mapContainerStyle = {
  height: "75vh",
  width: "100%",
  position: "absolute",
  top: "5rem",
  maxWidth: "inherit",
  right: ".1rem"
  // need to add max-width: inherit
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

function MapView({ heatMap, crimeData, queryType, twitterData }) {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
    libraries,

  });

  const [selected, setSelected] = React.useState(null);


  //we can retain state on 
  const mapRef = React.useRef()
  const onMapLoad = React.useCallback((map) => {
    mapRef.current = map
    console.log("LOADED MAP")
  }, [])

  const panTo = React.useCallback(({ lat, lng }) => {
    mapRef.current.panTo({ lat, lng })
    mapRef.current.setZoom(14)
  }, [])

  if (loadError) return "Error";
  if (!isLoaded) return "Loading...";

  return (
    <>
      <Search panTo={panTo} />
      <Locate panTo={panTo} />

      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        zoom={11}
        center={center}
        options={options}
        onLoad={onMapLoad}
      >
        {heatMap === 'Heat Map' ?
          <HeatmapLayer data={HeatMap(crimeData)} /> :
          <div>
            <DataPoints setSelected={setSelected} crimeData={crimeData} />
            <CrimeInfo selected={selected} setSelected={setSelected} />
          </div>}
          
          {queryType === 'Twitter Data' ?
          <TwitterPoints data={twitterData} /> :
          <></>}

      </GoogleMap>

    </>
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
    const points = crimeData.map((crime) => {
      {
        return <Circle
            key={crime.crime_id}
            radius={100}
            center={{
              lat: crime.latitude,
              lng: crime.longitude
            }}
            options={crime.sex === 'M' ? {
              strokeColor: "#0000FF",
              fillColor: "#0000FF",
              fillOpacity: 1
            } : {
              strokeColor: "#C71585",
              fillColor: "#C71585",
              fillOpacity: 1
            }}
            onClick={() => {
              setSelected(crime)
            }}
          />
      }
    })

    return points
  }

  else return null
}

function HeatMap(crimeData) {
  if (crimeData) {
    const points = crimeData.map((crime) => {
      return new window.google.maps.LatLng(crime.latitude, crime.longitude)
    })
    return points
  }
  else return []
}

function TwitterPoints(twitterData) {
  console.log(twitterData)
  if (twitterData) {
    const points = twitterData.data.map((crime) => {
      return <Marker
        key={crime.crime_id}
        position={{
          lat: crime.latitude,
          lng: crime.longitude
        }}
        icon={crime.sentiment === "Positive"
         ? {
          url: "/twitter-logoGreen.svg",
          scaledSize: new window.google.maps.Size(20, 20)
        } : {
          url: "/twitter-logoRed.svg",
          scaledSize: new window.google.maps.Size(20, 20)
        }}
        opacity={0.5}
      />
    })
    return points
  }
  else return null
}

function CrimeInfo({ selected, setSelected }) {
  return (
    selected ? (
      <InfoWindow
        position={{ lat: selected.latitude, lng: selected.longitude }}
        onCloseClick={() => {
          setSelected(null);
        }}
      >
        <div>
          <b>{selected.crime_type}</b>
          <p>Details</p>
          <ul>
            <li>Age: {selected.age}</li>
            <li>Sex: {selected.sex}</li>
            <li>Race: {selected.race}</li>
            <li>Time: {selected.time_occurred}</li>
          </ul>
        </div>
      </InfoWindow>
    ) : null
  )
}

export default React.memo(MapView)