import React from "react"
import { Tabs, Tab, Typography } from "@material-ui/core"
import { ListComponent } from "./ListComponent"
import { StatisticsPage } from "./StatisticsPage"

function TabPanel(props) {
  const { children, value, index, ...other } = props

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {children}
    </div>
  )
}

export default function TabComp({
  area,
  race,
  gender,
  crimeType,
  filteredData,
  listRefs,
  addToRefs,
  zoomLevel,
  setZoomLevel,
  setCenterCoordinates,
  setSelectedItem
}) {
  const [value, setValue] = React.useState(0)

  const handleChange = (event, newValue) => {
    setValue(newValue)
  }

  return (
    <div style={{ marginTop: 40, marginBottom: 20 }}>
      <Tabs
        value={value}
        onChange={handleChange}
        aria-label="simple tabs example"
        centered
        variant="fullWidth"
        TabIndicatorProps={{ style: { background: "#0EA7BC" } }}
      >
        <Tab label="Crime Incidents" />
        <Tab label="Crime Lab" />
      </Tabs>
      <Typography style={{ marginTop: 20, marginBottom: 10 }}>
        <span style={{ fontWeight: "bold" }}>{filteredData?.length}</span> crime
        incidents
      </Typography>

      <TabPanel value={value} index={0}>
        <ListComponent
          // open={open}
          // setOpen={setOpen}
          listRefs={listRefs}
          addToRefs={addToRefs}
          data={filteredData}
          zoomLevel={zoomLevel}
          setZoomLevel={setZoomLevel}
          setCenterCoordinates={setCenterCoordinates}
          setSelectedItem={setSelectedItem}
        />
      </TabPanel>

      <TabPanel value={value} index={1}>
        <StatisticsPage
          data={filteredData}
          area={area}
          race={race}
          gender={gender}
          crimeType={crimeType}
        />
      </TabPanel>
    </div>
  )
}
