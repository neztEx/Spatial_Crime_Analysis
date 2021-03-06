import React, { useState, useMemo, useRef, useEffect } from 'react'
import '../App.css'
import MapView from '../components/GoogleMap';
import { Container, Grid, CssBaseline } from "@material-ui/core"
import { ThemeProvider, createTheme } from "@material-ui/core/styles"
import { useMediaQuery, Button } from "@material-ui/core"
import { DateFilterComp } from "../components/DateFilterComp"
import { areaNameArr, raceDict, genderArr, crimeTypeArr, mapLayerArr, queryTypeArr } from "../components/Arr"
import SelectRaceComp from "../components/SelectRaceComp"
import SelectComp from "../components/SelectComp"
import pink from "@material-ui/core/colors/pink"
import cyan from "@material-ui/core/colors/blue"
import * as QueryServer from '../components/QueryServer'
import { Typography } from "@material-ui/core"



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
    { value: 'location', label: 'Location' }
  ]
  const [submit, setSubmit] = React.useCallback([])
  const [queryType, setQueryType] = React.useState("None");
  const [queryUpdated, setQueryUpdated] = React.useState(false);
  const [smallData, setSmallData] = useState([])
  const [data, setData] = useState([])
  const [twitterData, setTwitterData] = useState([])
  const [area, setArea] = useState("All Areas")
  const [race, setRace] = useState("All")
  const [mapLayer, setMapLayer] = useState("Data Points")
  const [age, setAge] = useState([0, 99])
  const [hour, setHour] = useState([0, 24])
  const [gender, setGender] = useState("All")
  const [selectedStartDate, setSelectedStartDate] = useState(
    new Date(2019, 0, 1)
  )
  const [selectedEndDate, setSelectedEndDate] = useState(new Date(2019, 0, 31))
  const [centerCoordinates, setCenterCoordinates] = useState({
    lat: 34.0722,
    lng: -118.37
  })
  const [zoomLevel, setZoomLevel] = useState(10)
  const [crimeType, setCrimeType] = useState("ALL CRIME TYPES")
  const raceArr = Object.keys(raceDict)
  const headerRef = useRef()
  const [start, setStart] = useState(0)
  const [end, setEnd] = useState(data.length > 1000 ? 1000 : 0)


  const onSelectChange = React.useEffect(() => {
    setQueryUpdated(!queryUpdated);
  }, [queryType])

  const onQueryTypeChange = React.useEffect(() => {
    QueryServer.twitter().then(result_json => setTwitterData(result_json))

  }, [queryType])

  const onSmallDataChange = React.useEffect(() => {
    console.log(start, end, smallData)
  }, [smallData])

  // old queries
  // const onQueryChange = React.useEffect(() => {
  //   QueryServer.generic(area, selectedStartDate, selectedEndDate, crimeType, gender, race).then(result_json => setData(result_json))

  // }, [area, selectedStartDate, selectedEndDate, crimeType, gender, race])

  const sendQuery = () => {
    console.log('sending query')
    QueryServer.generic(area, selectedStartDate, selectedEndDate, crimeType, gender, race).then(result_json => (setData(result_json), setEnd(result_json.length > 1000 ? 1000 : result_json.length), setStart(0), setSmallData(result_json.slice(start, (result_json.length > 1000 ? 1000 : result_json.length)))))
  }

  const onDataChange = React.useEffect(() => {
    console.log(data)
  }, [data])

  const handleChange = (selectedOption) => {
    setQueryType(selectedOption);
  }

  const next = () => {
    if (end == data.length) {
      setSmallData(data.slice(start, end))
      return
    }
    setStart(start + 1000)

    if (end + 1000 > data.length) {
      setEnd(data.length)
    }
    else {
      setEnd(end + 1000)
    }
    setSmallData(data.slice(start, end))
  }

  const prev = () => {
    if (start == 0) {
      setSmallData(data.slice(start, end))
      return
    }
    setEnd(end - 1000)
    if (start - 1000 < 0) {
      setStart(0)
    }
    else {
      setStart(start - 1000)
    }
    setSmallData(data.slice(start, end))
  }

  return (

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

                <Grid item xs={12}>
                  <SelectComp
                    title={"Select Crime Type"}
                    arr={crimeTypeArr}
                    foo={crimeType}
                    setFoo={setCrimeType}
                  />
                </Grid>

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
                <Grid item xs={12}>
                  <Button variant="contained" color="primary" type="submit" style={{ display: "flex", width: "100%" }}
                    onClick={sendQuery}>
                    Submit
                  </Button>
                </Grid>
                <Grid item xs={4}>
                  <Button variant="contained" type="Next" style={{ display: "flex", width: "100%" }}
                    onClick={prev}>
                    Prev
                  </Button>
                </Grid>
                <Grid item xs={4}>
                  {/* <div style={{
                    textAlign: "center",
                  }}>
                    
                    {start}...{end}
                  </div> */}
                  <Typography style={{
                    textAlign: "center",
                    marginTop: 10
                  }}>
                    {start}...{end}
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  <Button variant="contained" type="Prev" style={{ display: "flex", width: "100%" }}
                    onClick={next}>
                    Next
                  </Button>
                </Grid>
              </Grid>

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
            <MapView heatMap={mapLayer} crimeData={smallData} queryType={queryType} twitterData={twitterData} />

          </Grid>
        </Grid>
      </ThemeProvider>
    </div>
  )
}

export default Visualizations;
