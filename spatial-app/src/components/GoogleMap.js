import React from "react";
import {
  GoogleMap,
  useLoadScript,
  Marker,
  InfoWindow,
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
import mapStyles from "../mapStyles";
import "../App.css";

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
  loca: true
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

  //we can retain state on 
  const mapRef = React.useRef()
  const onMapLoad = React.useCallback((map) => {
    mapRef.current = map
  }, [])

  const panTo = React.useCallback(({lat, lng}) => {
    mapRef.current.panTo({lat,lng})
    mapRef.current.setZoom(14)
  }, [])

  if (loadError) return "Error";
  if (!isLoaded) return "Loading...";

  return (
    <div>
      <Search panTo={panTo}/>

      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        zoom={11}
        center={center}
        options={options}
        onLoad={onMapLoad}
      ></GoogleMap>
    </div>
  )
}

//Search bar
function Search({panTo}) {
  console.log(panTo)
  const { ready, value, suggestions: { status, data }, setValue, clearSuggestions } = usePlacesAutocomplete({
    requestOptions: {
      location: { lat: () => 34.0522, lng: () => -118.2437 },
      radius: 200 * 1000, // KM
    }
  })


  return (
    <div className="search">
      <Combobox onSelect={async (address) => {
        setValue(address, false)
        clearSuggestions()

        try {
          const result = await getGeocode({address})
          console.log(result[0])
          const {lat, lng} = await getLatLng(result[0])
          console.log(lat, lng)
          panTo({lat,lng})
        } catch (error) {
          console.log("error!")
          console.log(error)
        }
        console.log(address)
      }}>
        <ComboboxInput value={value} onChange={(e) => {
          setValue(e.target.value)
        }}
          disabled={!ready}
          placeholder="Enter Address"
        />
        <ComboboxPopover>
          {status == "OK" && 
          data.map(({id, description}) => (
          <ComboboxOption key={id} value={description}/>
          ))}
        </ComboboxPopover>
      </Combobox>
    </div>
  )
}
