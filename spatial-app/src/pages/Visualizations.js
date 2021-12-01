import React, { useState, useMemo, useRef, useEffect } from 'react'
import '../App.css'
import MapView from '../components/GoogleMap';
import { Container, Grid, CssBaseline } from "@material-ui/core"
import { ThemeProvider, createTheme } from "@material-ui/core/styles"
import { useMediaQuery } from "@material-ui/core"
import { DateFilterComp } from "../components/DateFilterComp"
import { Analysis } from "../components/Analysis"
import Map from '../components/Map'


import { areaNameArr, raceDict, genderArr, crimeTypeArr, mapLayerArr, queryTypeArr } from "../components/Arr"
import SelectRaceComp from "../components/SelectRaceComp"
import SelectComp from "../components/SelectComp"

import pink from "@material-ui/core/colors/pink"
import cyan from "@material-ui/core/colors/blue"


import * as QueryServer from '../components/QueryServer'


function Visualizations() {
  const prefersDarkMode = useMediaQuery("(prefers-color-scheme: light)")
  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          type: prefersDarkMode ? "dark" : "light",
          primary: cyan,
          secondary: pink
        }
      }),
    [prefersDarkMode]
  )
  

  const options = [
    {value: 'location', label: 'Location' }
  ]
  
  const [queryType, setQueryType] = React.useState("None");
  const [queryUpdated, setQueryUpdated] = React.useState(false);

  const [data, setData] = useState([])
  const [twitterData, setTwitterData] = useState([])
  const [area, setArea] = useState("All Areas")
  const [race, setRace] = useState("All")
  const [mapLayer, setMapLayer] = useState("Data Points")
  const [age, setAge] = useState([0, 99])
  const [hour, setHour] = useState([0, 24])
  const [gender, setGender] = useState("All")
  const [selectedStartDate, setSelectedStartDate] = useState(
    // new Date().setMonth(new Date().getMonth() - 1)
    new Date(2010,0,1)
  )
  const [selectedEndDate, setSelectedEndDate] = useState(new Date(2010,0,31))
  const [centerCoordinates, setCenterCoordinates] = useState({
    lat: 34.0722,
    lng: -118.37
  })
  const [zoomLevel, setZoomLevel] = useState(10)
  const [crimeType, setCrimeType] = useState("ALL CRIME TYPES")
  const raceArr = Object.keys(raceDict)
  const headerRef = useRef()


  const onSelectChange = React.useEffect(() => {
    setQueryUpdated(!queryUpdated);
  }, [queryType])

  const onQueryChange = React.useEffect(() => {
    QueryServer.generic(area,selectedStartDate,selectedEndDate, crimeType, gender, race).then(result_json => setData(result_json))
    
    // switch(queryType){
    //   case 'location':
    //     QueryServer.location(area).then(result_json => setData(result_json))
    //     break;
    //   default:
    //     QueryServer.location(area).then(result_json => setData(result_json))
    // }
  }, [area, selectedStartDate, selectedEndDate, crimeType, gender, race ])

  const onDataChange = React.useEffect(() => {
    console.log(data)
  }, [data])
  const handleChange = (selectedOption) => {
    setQueryType(selectedOption);
  }

  return (
    // <div>
    //   <MapView heatMap={heatMap} />
    //   <Switch onChange={(checked)=> {setheatMap(checked)}} checked={heatMap}/>
    // </div>
    <div style={{ width: "100vw", overflow: "hidden" }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Grid
          container
          spacing={0}
          style={{ width: "100vw", height: "100vh", overflow: "hidden" }}
        >
          <Grid
            item
            xs={12}
            md={4}
            style={{ height: "100vh", overflow: "auto" }}
          >
            <Container maxWidth="xs">
              {/* <Header headerRef={headerRef} /> */}
              <Grid container spacing={2}>
                <Grid item xs={12} style={{ marginTop: 20 }}>
                  <SelectComp
                    title={"Select Area"}
                    arr={areaNameArr}
                    foo={area}
                    setFoo={setArea}
                  />
                </Grid>
                <Grid item xs={12}>
                  <DateFilterComp
                    selectedStartDate={selectedStartDate}
                    selectedEndDate={selectedEndDate}
                    setSelectedStartDate={setSelectedStartDate}
                    setSelectedEndDate={setSelectedEndDate}
                  />
                </Grid>
                {/* <Grid item xs={12}>
                  <HourSliderComp hour={hour} setHour={setHour} />
                </Grid> */}
                <Grid item xs={12}>
                  <SelectComp
                    title={"Select Crime Type"}
                    arr={crimeTypeArr}
                    foo={crimeType}
                    setFoo={setCrimeType}
                  />
                </Grid>
                {/* <Grid item xs={12} style={{ marginBottom: 40 }}>
                  <div style={{ marginBottom: 5, fontSize: 10 }}>
                    Experimental Feature *
                  </div>
                  <ComboBox
                    arr={mocodesDict}
                    mocode={mocode}
                    setMocode={setMocode}
                  />
                </Grid> */}

                <Grid item xs={6}>
                  <SelectRaceComp
                    title={"Select Race of Victim"}
                    arr={raceArr}
                    foo={race}
                    setFoo={setRace}
                  />
                </Grid>
                <Grid item xs={6}>
                  <SelectComp
                    title={"Select Gender of Victim"}
                    arr={genderArr}
                    foo={gender}
                    setFoo={setGender}
                  />
                </Grid>
                <Grid item xs={6}>
                  <SelectComp
                    title={"Map Layers"}
                    arr={mapLayerArr}
                    foo={mapLayer}
                    setFoo={setMapLayer}
                  />
                </Grid>
                <Grid item xs={6}>
                  <SelectComp
                    title={"Data"}
                    arr={queryTypeArr}
                    foo={queryType}
                    setFoo={setQueryType}
                  />
                </Grid>
              </Grid>
              {/* <Grid item xs={12}>
                <AgeSliderComp age={age} setAge={setAge} />
              </Grid> */}

              {/* <TabComp
                area={area}
                race={race}
                gender={gender}
                crimeType={crimeType}
                filteredData={data}
                listRefs={listRefs}
                addToRefs={addToRefs}
                zoomLevel={zoomLevel}
                setZoomLevel={setZoomLevel}
                setCenterCoordinates={setCenterCoordinates}
                setSelectedItem={setSelectedItem}
              /> */}
              {/* <Resources /> */}
              {/* <Footer headerRef={headerRef} /> */}

            </Container>
          </Grid>

          <Grid
            item
            xs={12}
            md={8}
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center"
            }}
          >
            <MapView heatMap={mapLayer} crimeData={data} queryType={queryType} twitterData={twitterData}/>
            {/* <Switch onChange={(checked)=> {setheatMap(checked)}} checked={heatMap}/> */}
            {/* <Analysis
              data={data}
              area={area}
              race={race}
              gender={gender}
              crimeType={crimeType}
            /> */}
          </Grid>
        </Grid>
      </ThemeProvider>
    </div>
  )
}

export default Visualizations;
