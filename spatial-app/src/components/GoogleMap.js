import React from "react";
import {
  GoogleMap,
  useLoadScript,
  Marker,
  InfoWindow,
  Data,
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
import * as parksData from '../mockData/mock.json'
const libraries = ["places"];

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


  //we can retain state on 
  const mapRef = React.useRef()
  const onMapLoad = React.useCallback((map) => {
    mapRef.current = map
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
        {parksData.features.map((park) => (
          <Marker
            key={park.properties.PARK_ID}
            position={{
              lat: park.geometry.coordinates[1],
              lng: park.geometry.coordinates[0]
            }}
            icon={"https://storage.googleapis.com/support-kms-prod/SNP_2752125_en_v0"}
            animation='BOUNCE'
            onClick={()=>{
              setSelected(park)
            }}
          />
        ))}

        {selected ? (
          <InfoWindow
            position={{ lat: selected.geometry.coordinates[1], lng: selected.geometry.coordinates[0] }}
            onCloseClick={() => {
              setSelected(null);
            }}
          >
            <div>
              <h4>
                Crime
              </h4>
              <p>Spotted</p>
            </div>
          </InfoWindow>
        ) : null}

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
